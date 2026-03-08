"""Practice questions API router."""

from fastapi import APIRouter

from backend.models.schemas import PracticeRequest, PracticeResponse
from backend.services.practice_generator import generate_practice_questions

router = APIRouter(prefix="/api/practice", tags=["Practice"])


@router.post("", response_model=PracticeResponse)
async def practice(request: PracticeRequest):
    """Generate easy/medium/hard practice questions for a topic."""
    result = generate_practice_questions(request.topic, request.class_level)
    return PracticeResponse(**result)
