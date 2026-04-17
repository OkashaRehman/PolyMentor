import torch
import pytest
from src.models.error_detector import ErrorDetector


def test_error_detector_output_shape():
    model = ErrorDetector(num_labels=9)
    model.eval()
    batch_size = 2
    seq_len = 512
    input_ids = torch.randint(0, 1000, (batch_size, seq_len))
    attention_mask = torch.ones(batch_size, seq_len, dtype=torch.long)

    with torch.no_grad():
        logits = model(input_ids, attention_mask)

    assert logits.shape == (batch_size, 9)


def test_error_detector_predict_binary():
    model = ErrorDetector(num_labels=9)
    input_ids = torch.randint(0, 1000, (1, 512))
    attention_mask = torch.ones(1, 512, dtype=torch.long)
    preds = model.predict(input_ids, attention_mask)
    assert set(preds.unique().tolist()).issubset({0, 1})
