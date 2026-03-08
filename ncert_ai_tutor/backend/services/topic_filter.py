"""NCERT syllabus topic filter — checks if a question is within scope."""

import json
from pathlib import Path

_topics_cache: list[dict] | None = None


def _load_topics() -> list[dict]:
    """Load topics from ncert_topics.json (cached)."""
    global _topics_cache
    if _topics_cache is None:
        topics_path = Path(__file__).resolve().parent.parent.parent / "data" / "ncert_topics.json"
        with open(topics_path, encoding="utf-8") as f:
            data = json.load(f)
        _topics_cache = data["topics"]
    return _topics_cache


def detect_topic(question: str) -> dict | None:
    """Match a student question to an NCERT topic using keyword overlap.

    Returns the best-matching topic dict, or None if no match found.
    """
    topics = _load_topics()
    question_lower = question.lower()
    question_words = set(question_lower.split())

    best_match = None
    best_score = 0

    for topic in topics:
        keywords = [kw.strip() for kw in topic["keywords"].split(",")]
        # Score: whole-word matches get 2 points, substring matches get 1
        score = 0
        for kw in keywords:
            if kw in question_words:
                score += 2  # Exact word match
            elif len(kw) > 3 and kw in question_lower:
                score += 1  # Substring match (only for keywords > 3 chars)
        if score > best_score:
            best_score = score
            best_match = topic

    # Require meaningful match (at least one exact word or two substring matches)
    if best_score >= 2:
        return best_match
    return None


def is_within_syllabus(question: str) -> tuple[bool, dict | None]:
    """Check if a question falls within NCERT 9-10 syllabus.

    Returns (is_within, matched_topic_or_None).
    """
    topic = detect_topic(question)
    return (topic is not None, topic)


def get_out_of_syllabus_message() -> str:
    """Return the out-of-syllabus response in Hinglish."""
    return (
        "Ye topic NCERT class 9-10 syllabus mein nahi hai, yaar! 📚\n"
        "But tension mat le — main tujhe class 9-10 ke Science, Maths, "
        "aur Social Science mein help kar sakta hoon. Kuch aur puuchh! 💪"
    )


def get_topic_list_for_class(class_level: int) -> list[dict]:
    """Get all topics for a specific class level."""
    topics = _load_topics()
    return [t for t in topics if t["class_level"] == class_level]


def get_all_topic_names() -> list[str]:
    """Get a flat list of all topic names for dropdowns."""
    topics = _load_topics()
    return sorted(set(t["topic"] for t in topics))
