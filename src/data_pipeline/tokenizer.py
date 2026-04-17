from transformers import AutoTokenizer
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CodeTokenizer:
    """Wraps HuggingFace tokenizer for code snippets."""

    def __init__(
        self, model_name: str = "microsoft/codebert-base", max_length: int = 512
    ):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.max_length = max_length
        logger.info(f"Loaded tokenizer: {model_name}")

    def tokenize(self, code: str, language: str = "") -> dict:
        """Tokenize a code snippet. Language prefix helps the model."""
        prefix = f"<{language}> " if language else ""
        return self.tokenizer(
            prefix + code,
            max_length=self.max_length,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

    def batch_tokenize(self, codes: list, languages: list = None) -> dict:
        """Tokenize a batch of code snippets."""
        if languages is None:
            languages = [""] * len(codes)
        texts = [f"<{lang}> {code}" for lang, code in zip(languages, codes)]
        return self.tokenizer(
            texts,
            max_length=self.max_length,
            truncation=True,
            padding=True,
            return_tensors="pt",
        )
