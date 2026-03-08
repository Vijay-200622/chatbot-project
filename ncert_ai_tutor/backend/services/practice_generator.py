"""Practice question generator using LLM."""

from backend.services.llm_engine import generate_response
from data.system_prompts import PRACTICE_SYSTEM_PROMPT


def generate_practice_questions(topic: str, class_level: int = 10) -> dict:
    """Generate easy/medium/hard practice questions for a topic.

    Returns dict with keys: easy, medium, hard, raw_response.
    """
    prompt = (
        f"Generate 3 practice questions for NCERT Class {class_level} topic: {topic}\n"
        f"Follow the format exactly."
    )

    raw = generate_response(prompt, PRACTICE_SYSTEM_PROMPT, max_tokens=800)

    # Parse structured output
    questions = {"easy": "", "medium": "", "hard": "", "raw_response": raw}

    lines = raw.split("\n")
    current_key = None
    current_text = []

    for line in lines:
        line_lower = line.lower().strip()
        if any(m in line_lower for m in ["**easy**", "**easy:**", "easy:"]):
            if current_key:
                questions[current_key] = "\n".join(current_text).strip()
            current_key = "easy"
            # Extract text after the label
            for marker in ["**Easy:**", "**Easy:**", "Easy:", "**easy:**", "**easy**"]:
                if marker in line:
                    line = line.split(marker, 1)[-1]
                    break
            current_text = [line.strip()] if line.strip() else []
        elif any(m in line_lower for m in ["**medium**", "**medium:**", "medium:"]):
            if current_key:
                questions[current_key] = "\n".join(current_text).strip()
            current_key = "medium"
            for marker in ["**Medium:**", "**Medium:**", "Medium:", "**medium:**", "**medium**"]:
                if marker in line:
                    line = line.split(marker, 1)[-1]
                    break
            current_text = [line.strip()] if line.strip() else []
        elif any(m in line_lower for m in ["**hard**", "**hard:**", "hard:"]):
            if current_key:
                questions[current_key] = "\n".join(current_text).strip()
            current_key = "hard"
            for marker in ["**Hard:**", "**Hard:**", "Hard:", "**hard:**", "**hard**"]:
                if marker in line:
                    line = line.split(marker, 1)[-1]
                    break
            current_text = [line.strip()] if line.strip() else []
        elif current_key:
            current_text.append(line)

    if current_key:
        questions[current_key] = "\n".join(current_text).strip()

    return questions
