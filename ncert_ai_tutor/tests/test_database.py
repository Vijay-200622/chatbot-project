"""Tests for database CRUD operations."""

import sys
import os
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Override DB path before importing anything that uses settings
_test_db = os.path.join(tempfile.mkdtemp(), "test.db")
os.environ["DB_PATH"] = _test_db

# Patch settings before db module loads
from backend.config import settings
settings.db_path = _test_db

from database.db import init_db
from database.crud import (
    get_or_create_student,
    create_teacher,
    verify_teacher,
    insert_question,
    get_user_topic_history,
    log_question_for_streak,
    get_streak_data,
)

import pytest


@pytest.fixture(autouse=True, scope="session")
def setup_db():
    init_db()


def test_create_student():
    user = get_or_create_student("test_student")
    assert user["username"] == "test_student"
    assert user["role"] == "student"

    # Get same student again
    same_user = get_or_create_student("test_student")
    assert same_user["id"] == user["id"]


def test_create_teacher():
    teacher = create_teacher("test_teacher", "password123")
    assert teacher["username"] == "test_teacher"
    assert teacher["role"] == "teacher"


def test_verify_teacher():
    create_teacher("auth_teacher", "mypassword")
    result = verify_teacher("auth_teacher", "mypassword")
    assert result is not None
    assert result["username"] == "auth_teacher"

    # Wrong password
    result = verify_teacher("auth_teacher", "wrongpassword")
    assert result is None


def test_insert_and_query_questions():
    user = get_or_create_student("question_student")
    qid = insert_question(
        user_id=user["id"],
        question_text="What is photosynthesis?",
        detected_topic="Life Processes",
        response_text="Photosynthesis is...",
    )
    assert qid > 0

    history = get_user_topic_history(user["id"], "Life Processes")
    assert len(history) >= 1


def test_streaks():
    user = get_or_create_student("streak_student")

    # Log 3 questions
    for _ in range(3):
        log_question_for_streak(user["id"])

    data = get_streak_data(user["id"])
    assert data["today_count"] >= 3
    assert data["current_streak"] >= 1


if __name__ == "__main__":
    setup()
    test_create_student()
    test_create_teacher()
    test_verify_teacher()
    test_insert_and_query_questions()
    test_streaks()
    print("✅ All database tests passed!")
