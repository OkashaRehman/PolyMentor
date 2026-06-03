"""
PolyMentor FastAPI app.

PolyMentor is a Groq-powered coding tutor chatbot. It can teach concepts,
write code, review snippets, identify likely bugs, and propose corrected
examples across multiple languages.
"""

from __future__ import annotations

from typing import Literal, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.inference.pipeline import DEFAULT_MODEL, PolyMentorPipeline


app = FastAPI(
    title="PolyMentor API",
    description="Groq-powered chatbot for coding help, bug explanation, and programming lessons.",
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = PolyMentorPipeline.from_groq()


class ChatRequest(BaseModel):
    message: str = Field(..., description="Question or instruction for PolyMentor.")
    code: str = Field("", description="Optional code snippet to review or modify.")
    language: str = Field("python", description="Programming language for the code.")
    level: Literal["beginner", "intermediate", "advanced"] = Field(
        "beginner",
        description="Learner level used for explanation depth.",
    )


class ChatResponse(BaseModel):
    status: str
    answer: str
    language: str
    level: str
    model: str
    suspected_bugs: list[str]
    fixed_code: Optional[str]
    lesson: Optional[str]
    next_steps: list[str]
    elapsed_ms: float


@app.get("/")
def root():
    return {
        "name": "PolyMentor",
        "purpose": "A Groq-powered chatbot that teaches code and helps identify bugs.",
        "model": DEFAULT_MODEL,
        "docs": "/docs",
        "endpoints": {
            "chat": "POST /chat",
            "review_code": "POST /review",
            "teach": "POST /teach",
        },
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "provider": "groq",
        "model": pipeline.model,
        "requires": "GROQ_API_KEY",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = pipeline.chat(
        message=request.message,
        code=request.code,
        language=request.language,
        level=request.level,
    )
    return result.__dict__


@app.post("/review", response_model=ChatResponse)
def review_code(request: ChatRequest):
    result = pipeline.analyze(
        code=request.code,
        language=request.language,
        level=request.level,
        question=request.message
        or "Review this code, find likely bugs, explain them, and show a corrected version.",
    )
    return result.__dict__


@app.post("/teach", response_model=ChatResponse)
def teach(request: ChatRequest):
    lesson_prompt = (
        "Teach this programming topic with a short explanation, a small example, "
        "a common mistake, and a practice task. Topic: "
        f"{request.message}"
    )
    result = pipeline.chat(
        message=lesson_prompt,
        code=request.code,
        language=request.language,
        level=request.level,
    )
    return result.__dict__
