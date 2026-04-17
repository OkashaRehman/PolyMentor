import re
from src.utils.logger import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = [
    "id",
    "code",
    "language",
    "error_types",
    "difficulty",
    "explanation",
    "hint_steps",
    "concept_taught",
]

SUPPORTED_LANGUAGES = {"python", "javascript", "java", "cpp"}


class DataCleaner:
    """Validates and cleans raw data samples."""

    def clean(self, samples: list) -> list:
        cleaned = []
        seen_ids = set()

        for sample in samples:
            # Check required fields
            if not all(k in sample for k in REQUIRED_FIELDS):
                continue

            # Deduplicate by ID
            if sample["id"] in seen_ids:
                continue
            seen_ids.add(sample["id"])

            # Validate language
            if sample["language"] not in SUPPORTED_LANGUAGES:
                continue

            # Clean code: strip trailing whitespace per line
            sample["code"] = "\n".join(
                line.rstrip() for line in sample["code"].split("\n")
            )

            # Truncate very long snippets
            if len(sample["code"]) > 4000:
                continue

            cleaned.append(sample)

        logger.info(f"Cleaned: {len(cleaned)}/{len(samples)} samples kept")
        return cleaned
