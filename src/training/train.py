import json
import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import get_linear_schedule_with_warmup
from src.models.model_factory import ModelFactory
from src.data_pipeline.tokenizer import CodeTokenizer
from src.training.loss_functions import FocalLoss
from src.training.metrics import compute_metrics
from src.utils.config_loader import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CodeErrorDataset(Dataset):
    def __init__(self, data_path: str, tokenizer: CodeTokenizer, error_types: dict):
        with open(data_path) as f:
            self.data = json.load(f)
        self.tokenizer = tokenizer
        self.error_types = error_types
        self.num_labels = len(error_types)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        tokens = self.tokenizer.tokenize(sample["code"], sample["language"])
        label_vector = torch.zeros(self.num_labels)
        for error in sample.get("error_types", []):
            if error in self.error_types:
                label_vector[self.error_types[error]] = 1.0

        return {
            "input_ids": tokens["input_ids"].squeeze(0),
            "attention_mask": tokens["attention_mask"].squeeze(0),
            "labels": label_vector,
        }


def train():
    config = load_config("configs/training_config.yaml")
    model_config = load_config("configs/model_config.yaml")

    with open("data/labels/error_types.json") as f:
        error_types = json.load(f)

    factory = ModelFactory()
    model = factory.build_error_detector()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    tokenizer = CodeTokenizer(model_config["model"]["backbone"])

    train_dataset = CodeErrorDataset(
        "data/processed/train.json", tokenizer, error_types
    )
    val_dataset = CodeErrorDataset("data/processed/val.json", tokenizer, error_types)

    tc = config["training"]
    train_loader = DataLoader(train_dataset, batch_size=tc["batch_size"], shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=tc["batch_size"])

    optimizer = AdamW(
        model.parameters(), lr=tc["learning_rate"], weight_decay=tc["weight_decay"]
    )
    total_steps = len(train_loader) * tc["epochs"]
    warmup_steps = int(total_steps * tc["warmup_ratio"])
    scheduler = get_linear_schedule_with_warmup(optimizer, warmup_steps, total_steps)
    criterion = FocalLoss()

    best_f1 = 0.0

    for epoch in range(tc["epochs"]):
        model.train()
        total_loss = 0

        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()

        # Validation
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for batch in val_loader:
                input_ids = batch["input_ids"].to(device)
                attention_mask = batch["attention_mask"].to(device)
                logits = model(input_ids, attention_mask)
                preds = (torch.sigmoid(logits) >= 0.5).int().cpu().numpy()
                all_preds.append(preds)
                all_labels.append(batch["labels"].numpy())

        all_preds = np.vstack(all_preds)
        all_labels = np.vstack(all_labels)
        metrics = compute_metrics(all_preds, all_labels)

        logger.info(
            f"Epoch {epoch+1}/{tc['epochs']} | "
            f"Loss: {total_loss/len(train_loader):.4f} | "
            f"F1: {metrics['f1_micro']:.4f}"
        )

        if metrics["f1_micro"] > best_f1:
            best_f1 = metrics["f1_micro"]
            factory.save_model(model, "models_saved/best_mentor_model.pt")
            logger.info(f"✅ New best model saved (F1: {best_f1:.4f})")


if __name__ == "__main__":
    train()
