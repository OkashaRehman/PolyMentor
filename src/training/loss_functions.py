import torch
import torch.nn as nn


class FocalLoss(nn.Module):
    """
    Focal Loss for multi-label classification.
    Helps when error types are imbalanced (e.g., syntax errors are much more common).
    """

    def __init__(self, gamma: float = 2.0, pos_weight: torch.Tensor = None):
        super().__init__()
        self.gamma = gamma
        self.bce = nn.BCEWithLogitsLoss(pos_weight=pos_weight, reduction="none")

    def forward(self, logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
        bce_loss = self.bce(logits, targets.float())
        probs = torch.sigmoid(logits)
        pt = targets * probs + (1 - targets) * (1 - probs)
        focal_weight = (1 - pt) ** self.gamma
        return (focal_weight * bce_loss).mean()
