import json
import random
from pathlib import Path
from src.data_pipeline.collector import DataCollector
from src.data_pipeline.cleaner import DataCleaner
from src.utils.logger import get_logger

logger = get_logger(__name__)


class DatasetBuilder:
    """Builds train/val/test splits and writes them to data/processed/."""

    def __init__(
        self,
        raw_dir: str = "data/raw",
        output_dir: str = "data/processed",
        train_ratio: float = 0.8,
        val_ratio: float = 0.1,
        seed: int = 42,
    ):
        self.raw_dir = raw_dir
        self.output_dir = Path(output_dir)
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.seed = seed

    def build(self):
        """Full pipeline: collect → clean → split → save."""
        collector = DataCollector(self.raw_dir)
        cleaner = DataCleaner()

        samples = collector.load_all_samples()
        samples = cleaner.clean(samples)

        random.seed(self.seed)
        random.shuffle(samples)

        n = len(samples)
        n_train = int(n * self.train_ratio)
        n_val = int(n * self.val_ratio)

        splits = {
            "train": samples[:n_train],
            "val": samples[n_train : n_train + n_val],
            "test": samples[n_train + n_val :],
        }

        self.output_dir.mkdir(parents=True, exist_ok=True)
        for split_name, split_data in splits.items():
            output_path = self.output_dir / f"{split_name}.json"
            with open(output_path, "w") as f:
                json.dump(split_data, f, indent=2)
            logger.info(f"Saved {len(split_data)} samples to {output_path}")

        return splits


if __name__ == "__main__":
    builder = DatasetBuilder()
    builder.build()
