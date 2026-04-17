from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.inference.pipeline import PolyMentorPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="PolyMentor API",
    description="AI-powered coding mentor — error detection, explanation, and hints.",
    version="0.1.0",
)

# Load the model once at startup
pipeline = None


@app.on_event("startup")
def load_model():
    global pipeline
    pipeline = PolyMentorPipeline.from_pretrained("models_saved/best_mentor_model.pt")
    logger.info("PolyMentor pipeline loaded and ready.")


class AnalyzeRequest(BaseModel):
    code: str
    language: str = "python"
    level: str = "beginner"


class AnalyzeResponse(BaseModel):
    error_types: list
    primary_error: str
    explanation: str
    hints: list
    concept_taught: str
    quality_score: int


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet.")

    try:
        result = pipeline.analyze(
            code=request.code, language=request.language, level=request.level
        )
        return AnalyzeResponse(
            error_types=result.error_types,
            primary_error=result.primary_error,
            explanation=result.explanation,
            hints=result.hints,
            concept_taught=result.concept_taught,
            quality_score=result.quality_score,
        )
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": pipeline is not None}
