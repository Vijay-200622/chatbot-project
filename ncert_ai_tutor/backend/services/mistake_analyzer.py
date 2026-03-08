"""Mistake analyzer — analyzes incorrect student answers."""

from backend.services.llm_engine import generate_response
from data.system_prompts import MISTAKE_ANALYSIS_PROMPT


def analyze_mistake(
    student_answer: str,
    question: str = "",
    topic: str = "",
) -> str:
    """Analyze a student's incorrect answer and provide guidance.

    Returns the analysis text in Hinglish/Tanglish style.
    """
    context_parts = []
    if topic:
        context_parts.append(f"Topic: {topic}")
    if question:
        context_parts.append(f"Question: {question}")
    context_parts.append(f"Student's Answer: {student_answer}")

    user_message = "\n".join(context_parts)
    user_message += (
        "\n\nAnalyze this answer. Point out mistakes, explain correct approach, "
        "and give tips to avoid this mistake in the exam."
    )

    return generate_response(user_message, MISTAKE_ANALYSIS_PROMPT, max_tokens=800)
