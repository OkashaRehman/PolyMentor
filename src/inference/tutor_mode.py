#!/usr/bin/env python3
"""Command-line entrypoint for the Groq-powered PolyMentor tutor."""

import argparse
import sys

from src.inference.pipeline import DEFAULT_MODEL, PolyMentorPipeline
from src.inference.tutor import TutorSession
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="PolyMentor Groq Coding Tutor")
    parser.add_argument("--language", default="python", help="Default programming language.")
    parser.add_argument(
        "--level",
        default="beginner",
        choices=["beginner", "intermediate", "advanced"],
        help="Explanation depth.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Groq model name.")
    args = parser.parse_args()

    try:
        pipeline = PolyMentorPipeline.from_groq(model=args.model)
        TutorSession(pipeline=pipeline, language=args.language, level=args.level).start()
    except Exception as exc:
        print(f"PolyMentor failed to start: {exc}")
        logger.error("Tutor mode error: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
