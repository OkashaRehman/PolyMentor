"""
Compatibility model factory for the Groq-powered PolyMentor plan.

PolyMentor no longer loads a local CodeBERT/CodeT5 checkpoint for normal use.
The active model is a Groq-hosted chat model wrapped by PolyMentorPipeline.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.inference.pipeline import DEFAULT_MODEL, PolyMentorPipeline


@dataclass
class ModelBundle:
    pipeline: PolyMentorPipeline
    provider: str = "groq"
    model: str = DEFAULT_MODEL


class ModelFactory:
    @classmethod
    def from_groq(cls, model: str = DEFAULT_MODEL, api_key: Optional[str] = None) -> ModelBundle:
        pipeline = PolyMentorPipeline.from_groq(model=model, api_key=api_key)
        return ModelBundle(pipeline=pipeline, model=model)

    @classmethod
    def from_checkpoint(cls, *_args, **_kwargs) -> ModelBundle:
        """Backward-compatible alias. Local checkpoints are no longer required."""
        return cls.from_groq()

    @classmethod
    def build_chatbot(cls, model: str = DEFAULT_MODEL) -> PolyMentorPipeline:
        return PolyMentorPipeline.from_groq(model=model)
