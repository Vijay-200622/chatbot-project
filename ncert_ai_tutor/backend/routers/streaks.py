"""Study streaks API router."""

from fastapi import APIRouter

from backend.models.schemas import StreakResponse
from database.crud import get_streak_data, get_or_create_student

router = APIRouter(prefix="/api/streaks", tags=["Streaks"])


@router.get("/{username}", response_model=StreakResponse)
async def get_streaks(username: str):
    """Get streak information for a student."""
    user = get_or_create_student(username)
    data = get_streak_data(user["id"])
    return StreakResponse(**data)
