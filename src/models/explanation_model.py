import torch
from transformers import T5ForConditionalGeneration, AutoTokenizer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ExplanationModel:
    """
    Fine-tuned CodeT5 model that generates natural language explanations
    for code errors. Input: code snippet + error type. Output: explanation string.
    """

    def __init__(self, model_name: str = "Salesforce/codet5-base", device: str = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name).to(
            self.device
        )
        logger.info(f"ExplanationModel loaded: {model_name} on {self.device}")

    def generate(self, code: str, error_label: str, max_length: int = 256) -> str:
        """Generate a plain-English explanation for a code error."""
        prompt = f"explain error: [{error_label}]\ncode:\n{code}"
        inputs = self.tokenizer(
            prompt, return_tensors="pt", max_length=512, truncation=True
        ).to(self.device)

        with torch.no_grad():
            output_ids = self.model.generate(
                **inputs, max_length=max_length, num_beams=4, early_stopping=True
            )

        return self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

    def load_fine_tuned(self, checkpoint_path: str):
        """Load fine-tuned weights from a local checkpoint."""
        self.model = T5ForConditionalGeneration.from_pretrained(checkpoint_path).to(
            self.device
        )
        self.tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)
        logger.info(f"Loaded fine-tuned explanation model from {checkpoint_path}")
