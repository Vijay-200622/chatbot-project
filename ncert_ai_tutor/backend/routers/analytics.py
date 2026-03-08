"""Teacher analytics API router."""

from fastapi import APIRouter

from database.crud import get_weekly_topic_frequency, get_confused_topics, get_daily_question_counts

router = APIRouter(prefix="/api/analytics", tags=["Analytics"])


@router.get("/weekly-topics")
async def weekly_topics():
    """Get top asked topics for the last 7 days."""
    return get_weekly_topic_frequency()


@router.get("/confused-topics")
async def confused_topics():
    """Get most confusing topics (repeatedly asked by same users)."""
    return get_confused_topics()


@router.get("/daily-counts")
async def daily_counts(days: int = 30):
    """Get daily question counts for charting."""
    return get_daily_question_counts(min(days, 90))
