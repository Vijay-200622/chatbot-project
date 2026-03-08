"""Adaptive difficulty engine — adjusts explanation complexity based on repeat questions."""

from database.crud import get_user_topic_history
from data.system_prompts import DIFFICULTY_HINTS


def get_difficulty_level(user_id: int, topic: str) -> tuple[str, str]:
    """Determine difficulty level based on how many times user asked about this topic.

    Returns (level_key, hint_text_for_prompt).
    """
    history = get_user_topic_history(user_id, topic, days=7)
    ask_count = len(history)

    if ask_count == 0:
        return "normal", DIFFICULTY_HINTS["normal"]
    elif ask_count == 1:
        return "simpler", DIFFICULTY_HINTS["simpler"]
    else:
        return "step_by_step", DIFFICULTY_HINTS["step_by_step"]
