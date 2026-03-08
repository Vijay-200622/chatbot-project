"""CRUD operations for all database tables."""

import bcrypt
from datetime import date, datetime, timedelta
from typing import Optional

from database.db import get_connection


# ── Users ─────────────────────────────────────────────────────────

def get_or_create_student(username: str) -> dict:
    """Get existing student or create a new one. Returns user dict."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND role = 'student'",
            (username,)
        ).fetchone()
        if row:
            return dict(row)

        conn.execute(
            "INSERT INTO users (username, role) VALUES (?, 'student')",
            (username,)
        )
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND role = 'student'",
            (username,)
        ).fetchone()
        return dict(row)


def create_teacher(username: str, password: str) -> dict:
    """Create a teacher account with hashed password."""
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO users (username, role, password_hash) VALUES (?, 'teacher', ?)",
            (username, password_hash)
        )
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND role = 'teacher'",
            (username,)
        ).fetchone()
        return dict(row)


def verify_teacher(username: str, password: str) -> Optional[dict]:
    """Verify teacher credentials. Returns user dict or None."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ? AND role = 'teacher'",
            (username,)
        ).fetchone()
        if row and bcrypt.checkpw(password.encode(), row["password_hash"].encode()):
            return dict(row)
        return None


# ── Questions ─────────────────────────────────────────────────────

def insert_question(
    user_id: int,
    question_text: str,
    detected_topic: str = None,
    detected_language: str = "hinglish",
    response_text: str = None,
    difficulty_level: str = "normal",
) -> int:
    """Insert a question record and return its ID."""
    with get_connection() as conn:
        cursor = conn.execute(
            """INSERT INTO questions
               (user_id, question_text, detected_topic, detected_language, response_text, difficulty_level)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, question_text, detected_topic, detected_language, response_text, difficulty_level),
        )
        return cursor.lastrowid


def get_user_topic_history(user_id: int, topic: str, days: int = 7) -> list[dict]:
    """Get user's recent questions on a specific topic."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT * FROM questions
               WHERE user_id = ? AND detected_topic = ? AND created_at >= ?
               ORDER BY created_at DESC""",
            (user_id, topic, cutoff),
        ).fetchall()
        return [dict(r) for r in rows]


def get_weekly_topic_frequency() -> list[dict]:
    """Get topic frequency for the last 7 days (for analytics)."""
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT detected_topic as topic, COUNT(*) as count
               FROM questions
               WHERE created_at >= ? AND detected_topic IS NOT NULL
               GROUP BY detected_topic
               ORDER BY count DESC
               LIMIT 20""",
            (cutoff,),
        ).fetchall()
        return [dict(r) for r in rows]


def get_confused_topics(limit: int = 10) -> list[dict]:
    """Get topics asked repeatedly by same users (indicates confusion)."""
    cutoff = (datetime.now() - timedelta(days=7)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT detected_topic as topic, user_id,
                      COUNT(*) as repeat_count
               FROM questions
               WHERE created_at >= ? AND detected_topic IS NOT NULL
               GROUP BY detected_topic, user_id
               HAVING COUNT(*) >= 2
               ORDER BY repeat_count DESC
               LIMIT ?""",
            (cutoff, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def get_daily_question_counts(days: int = 30) -> list[dict]:
    """Get daily question counts for the last N days."""
    cutoff = (datetime.now() - timedelta(days=days)).isoformat()
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT DATE(created_at) as date, COUNT(*) as count
               FROM questions
               WHERE created_at >= ?
               GROUP BY DATE(created_at)
               ORDER BY date""",
            (cutoff,),
        ).fetchall()
        return [dict(r) for r in rows]


# ── Streaks ───────────────────────────────────────────────────────

def log_question_for_streak(user_id: int) -> dict:
    """Increment today's question count and update streak status."""
    today = date.today().isoformat()
    with get_connection() as conn:
        # Upsert today's record
        conn.execute(
            """INSERT INTO streaks (user_id, date, question_count, streak_active)
               VALUES (?, ?, 1, 0)
               ON CONFLICT(user_id, date)
               DO UPDATE SET question_count = question_count + 1""",
            (user_id, today),
        )
        # Check if threshold met (3 questions)
        row = conn.execute(
            "SELECT * FROM streaks WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone()

        if row and row["question_count"] >= 3:
            conn.execute(
                "UPDATE streaks SET streak_active = 1 WHERE user_id = ? AND date = ?",
                (user_id, today),
            )

        return dict(conn.execute(
            "SELECT * FROM streaks WHERE user_id = ? AND date = ?",
            (user_id, today),
        ).fetchone())


def get_streak_data(user_id: int) -> dict:
    """Get user's streak information."""
    with get_connection() as conn:
        # Get all active streak days ordered by date
        rows = conn.execute(
            """SELECT date, question_count, streak_active
               FROM streaks
               WHERE user_id = ?
               ORDER BY date DESC""",
            (user_id,),
        ).fetchall()

        if not rows:
            return {"current_streak": 0, "longest_streak": 0, "today_count": 0, "history": []}

        history = [dict(r) for r in rows]

        # Calculate current streak (consecutive active days ending today or yesterday)
        today = date.today()
        current_streak = 0
        check_date = today
        for row in history:
            row_date = date.fromisoformat(row["date"])
            if row_date == check_date and row["streak_active"]:
                current_streak += 1
                check_date -= timedelta(days=1)
            elif row_date < check_date:
                break

        # Longest streak
        longest = 0
        temp = 0
        all_dates = sorted(history, key=lambda x: x["date"])
        for i, row in enumerate(all_dates):
            if row["streak_active"]:
                temp += 1
                longest = max(longest, temp)
            else:
                temp = 0

        # Today's count
        today_record = next((r for r in history if r["date"] == today.isoformat()), None)
        today_count = today_record["question_count"] if today_record else 0

        return {
            "current_streak": current_streak,
            "longest_streak": longest,
            "today_count": today_count,
            "history": history[:30],  # Last 30 days
        }


# ── Topics (seed data) ───────────────────────────────────────────

def seed_topics_from_json(topics_data: list[dict]):
    """Seed topics table from ncert_topics.json."""
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
        if count > 0:
            return  # Already seeded

        for t in topics_data:
            conn.execute(
                "INSERT INTO topics (class_level, subject, chapter, topic, keywords) VALUES (?, ?, ?, ?, ?)",
                (t["class_level"], t["subject"], t["chapter"], t["topic"], t["keywords"]),
            )


def get_all_topics() -> list[dict]:
    """Get all NCERT topics."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM topics ORDER BY class_level, subject, chapter").fetchall()
        return [dict(r) for r in rows]


def get_topics_by_class(class_level: int) -> list[dict]:
    """Get topics for a specific class."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM topics WHERE class_level = ? ORDER BY subject, chapter",
            (class_level,),
        ).fetchall()
        return [dict(r) for r in rows]
