import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score


def compute_metrics(predictions: np.ndarray, labels: np.ndarray) -> dict:
    """Compute multi-label classification metrics."""
    return {
        "f1_micro": f1_score(labels, predictions, average="micro", zero_division=0),
        "f1_macro": f1_score(labels, predictions, average="macro", zero_division=0),
        "precision_micro": precision_score(
            labels, predictions, average="micro", zero_division=0
        ),
        "recall_micro": recall_score(
            labels, predictions, average="micro", zero_division=0
        ),
    }
