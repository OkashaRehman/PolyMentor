import os
import torch
from src.models.error_detector import ErrorDetector
from src.models.model_factory import ModelFactory, DEFAULT_CHECKPOINT
from src.utils.config_loader import load_config
import json

def create_fake_checkpoint():
    os.makedirs(os.path.dirname(DEFAULT_CHECKPOINT), exist_ok=True)
    
    with open("data/labels/error_types.json") as f:
        error_types = json.load(f)
    
    model_config = load_config("configs/model_config.yaml")
    
    detector = ErrorDetector(num_labels=len(error_types), model_id=model_config["model"]["backbone"])
    
    bundle_data = {
        "detector_num_labels": len(error_types),
        "detector_model_id": model_config["model"]["backbone"],
        "detector_tokenizer_id": model_config["model"]["backbone"],
        "detector_state_dict": detector.state_dict(),
        "explanation_model_id": "Salesforce/codet5-small", # Make it load small model fast
        "hint_model_id": "Salesforce/codet5-small",
    }
    
    torch.save(bundle_data, DEFAULT_CHECKPOINT)
    print("Dummy checkpoint created at", DEFAULT_CHECKPOINT)

if __name__ == "__main__":
    create_fake_checkpoint()