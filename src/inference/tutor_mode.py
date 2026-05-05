#!/usr/bin/env python3
"""
src/inference/tutor_mode.py
---------------------------
Command-line interface for the interactive tutoring mode.

This is the entry point for the CLI tutor. It parses command-line arguments
and launches an interactive tutoring session.

Usage:
    python src/inference/tutor_mode.py --model PATH [--language LANG] [--level LEVEL] [--log-file LOG]
"""

import argparse
import os
import sys
from pathlib import Path

from src.inference.pipeline import PolyMentorPipeline
from src.inference.tutor import TutorSession
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """Main entry point for tutor mode CLI."""
    parser = argparse.ArgumentParser(
        description="PolyMentor Interactive Tutor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python src/inference/tutor_mode.py --model models_saved/best_mentor_model.pt
  python src/inference/tutor_mode.py --model models_saved/best_mentor_model.pt --language python --level beginner
        """,
    )

    parser.add_argument(
        "--model",
        type=str,
        required=True,
        help="Path to the model checkpoint (e.g., models_saved/best_mentor_model.pt)",
    )

    parser.add_argument(
        "--language",
        type=str,
        default="python",
        choices=["python", "javascript", "cpp", "java"],
        help="Default programming language (default: python)",
    )

    parser.add_argument(
        "--level",
        type=str,
        default="beginner",
        choices=["beginner", "intermediate", "advanced"],
        help="Default learner level (default: beginner)",
    )

    parser.add_argument(
        "--log-file",
        type=str,
        default=None,
        help="Optional log file path (default: no logging to file)",
    )

    args = parser.parse_args()

    # Validate model path
    model_path = Path(args.model)
    if not model_path.exists():
        print(f"❌ Error: Model not found at {model_path}")
        print(f"   Please train a model first: bash scripts/train.sh")
        sys.exit(1)

    try:
        logger.info(f"Loading model from {model_path}...")
        pipeline = PolyMentorPipeline.from_pretrained(str(model_path))
        logger.info("✅ Model loaded successfully")

        # Create and start tutor session
        session = TutorSession(
            pipeline=pipeline,
            language=args.language,
            level=args.level,
        )

        logger.info(f"Starting tutor session (language={args.language}, level={args.level})")
        session.start()
        logger.info("Session ended")

    except FileNotFoundError as e:
        print(f"❌ Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Tutor mode error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
