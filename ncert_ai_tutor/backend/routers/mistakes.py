"""Mistake analyzer API router."""

from fastapi import APIRouter

from backend.models.schemas import MistakeRequest, MistakeResponse
from backend.services.mistake_analyzer import analyze_mistake

router = APIRouter(prefix="/api/analyze-mistake", tags=["Mistake Analyzer"])


@router.post("", response_model=MistakeResponse)
async def analyze(request: MistakeRequest):
    """Analyze a student's incorrect answer."""
    analysis = analyze_mistake(
        student_answer=request.student_answer,
        question=request.question,
        topic=request.topic,
    )
    return MistakeResponse(analysis=analysis)
