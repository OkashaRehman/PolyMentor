import json
import torch
import numpy as np
from torch.utils.data import DataLoader
from src.models.model_factory import ModelFactory
from src.data_pipeline.tokenizer import CodeTokenizer
from src.training.train import CodeErrorDataset
from src.training.metrics import compute_metrics
from src.utils.config_loader import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def evaluate():
    model_config = load_config("configs/model_config.yaml")

    with open("data/labels/error_types.json") as f:
        error_types = json.load(f)

    factory = ModelFactory()
    model = factory.load_error_detector("models_saved/best_mentor_model.pt")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    tokenizer = CodeTokenizer(model_config["model"]["backbone"])
    test_dataset = CodeErrorDataset("data/processed/test.json", tokenizer, error_types)
    test_loader = DataLoader(test_dataset, batch_size=16)

    all_preds, all_labels = [], []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            logits = model(input_ids, attention_mask)
            preds = (torch.sigmoid(logits) >= 0.5).int().cpu().numpy()
            all_preds.append(preds)
            all_labels.append(batch["labels"].numpy())

    all_preds = np.vstack(all_preds)
    all_labels = np.vstack(all_labels)
    metrics = compute_metrics(all_preds, all_labels)

    logger.info("=" * 50)
    logger.info("📊 EVALUATION RESULTS")
    for k, v in metrics.items():
        logger.info(f"  {k}: {v:.4f}")
    logger.info("=" * 50)

    return metrics


if __name__ == "__main__":
    evaluate()
