"""
Groq model adapter for PolyMentor.

The "model" in the current PolyMentor plan is not a local checkpoint. It is a
Groq-hosted chat model wrapped by src.inference.pipeline.PolyMentorPipeline.
This module exists so older code that imports from src.models can still find a
model-facing abstraction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.inference.pipeline import DEFAULT_MODEL, PolyMentorPipeline


@dataclass
class GroqModelConfig:
    model: str = DEFAULT_MODEL
    temperature: float = 0.25
    max_tokens: int = 1800


class GroqMentorModel:
    def __init__(self, config: Optional[GroqModelConfig] = None) -> None:
        self.config = config or GroqModelConfig()
        self.pipeline = PolyMentorPipeline(
            model=self.config.model,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
        )

    def chat(self, message: str, code: str = "", language: str = "python", level: str = "beginner"):
        return self.pipeline.chat(message=message, code=code, language=language, level=level)
