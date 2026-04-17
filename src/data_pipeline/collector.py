import json
from pathlib import Path
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DataCollector:
    """Loads and normalizes raw code samples into the unified schema."""

    def __init__(self, raw_dir: str = "data/raw"):
        self.raw_dir = Path(raw_dir)

    def load_json_file(self, filepath: str) -> list:
        with open(filepath, "r") as f:
            return json.load(f)

    def load_all_samples(self) -> list:
        """Load all .json files from data/raw/ recursively."""
        samples = []
        for json_file in self.raw_dir.rglob("*.json"):
            try:
                data = self.load_json_file(json_file)
                if isinstance(data, list):
                    samples.extend(data)
                    logger.info(f"Loaded {len(data)} samples from {json_file}")
            except Exception as e:
                logger.warning(f"Failed to load {json_file}: {e}")
        return samples
