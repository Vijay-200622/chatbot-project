"""Pydantic request/response models for all API endpoints."""

from pydantic import BaseModel, Field
from typing import Optional


# ── Chat ──────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    username: str = Field(..., min_length=1, max_length=100)
    conversation_history: list[dict] = Field(default_factory=list)


class ChatResponse(BaseModel):
    answer: str
    detected_topic: Optional[str] = None
    detected_language: str = "english"
    difficulty_level: str = "normal"
    within_syllabus: bool = True


# ── Voice ─────────────────────────────────────────────────────────

class VoiceRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    language: Optional[str] = None


# ── Practice ──────────────────────────────────────────────────────

class PracticeRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)
    class_level: int = Field(default=10, ge=9, le=10)


class PracticeResponse(BaseModel):
    easy: str
    medium: str
    hard: str
    raw_response: str


# ── Concept Map ───────────────────────────────────────────────────

class ConceptMapRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=200)


class ConceptMapResponse(BaseModel):
    svg: str
    edges: list[list[str]]
    dot_source: str


# ── Mistake Analyzer ─────────────────────────────────────────────

class MistakeRequest(BaseModel):
    student_answer: str = Field(..., min_length=1, max_length=3000)
    question: str = Field(default="", max_length=1000)
    topic: str = Field(default="", max_length=200)


class MistakeResponse(BaseModel):
    analysis: str


# ── Streaks ───────────────────────────────────────────────────────

class StreakResponse(BaseModel):
    current_streak: int
    longest_streak: int
    today_count: int
    history: list[dict]


# ── Auth ──────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=200)


class LoginResponse(BaseModel):
    success: bool
    message: str
    user_id: Optional[int] = None


# ── Analytics ─────────────────────────────────────────────────────

class TopicFrequency(BaseModel):
    topic: str
    count: int


class ConfusedTopic(BaseModel):
    topic: str
    user_id: int
    repeat_count: int


class DailyCount(BaseModel):
    date: str
    count: int
