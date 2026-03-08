"""Chat API router."""

from fastapi import APIRouter
from fastapi.responses import Response

from backend.models.schemas import ChatRequest, ChatResponse, VoiceRequest
from backend.services.llm_engine import generate_with_context
from backend.services.topic_filter import is_within_syllabus
from backend.services.adaptive_engine import get_difficulty_level
from backend.services.language_detector import detect_input_language
from backend.services.voice_engine import get_audio_bytes
from data.system_prompts import CHAT_SYSTEM_PROMPT, LANGUAGE_INSTRUCTIONS
from database.crud import get_or_create_student, insert_question, log_question_for_streak

router = APIRouter(prefix="/api/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a student's question and return AI response."""
    user = get_or_create_student(request.username)
    user_id = user["id"]

    # Detect input language (tanglish / hinglish / english)
    detected_lang = detect_input_language(request.question)

    # Try to detect NCERT topic via keywords (soft hint, not a hard block)
    within_syllabus, matched_topic = is_within_syllabus(request.question)
    topic_name = matched_topic["topic"] if matched_topic else "General"

    # Get adaptive difficulty based on topic history
    difficulty_level, difficulty_hint = get_difficulty_level(user_id, topic_name)

    # Build system prompt with language instruction and difficulty hint
    language_instruction = LANGUAGE_INSTRUCTIONS.get(detected_lang, LANGUAGE_INSTRUCTIONS["english"])
    system_prompt = CHAT_SYSTEM_PROMPT.format(
        detected_language=detected_lang.upper(),
        language_instruction=language_instruction,
        difficulty_hint=difficulty_hint,
    )

    answer = generate_with_context(
        user_message=request.question,
        system_prompt=system_prompt,
        conversation_history=request.conversation_history,
    )

    # Save to database
    insert_question(
        user_id=user_id,
        question_text=request.question,
        detected_topic=topic_name,
        response_text=answer,
        difficulty_level=difficulty_level,
    )

    # Log for streak tracking
    log_question_for_streak(user_id)

    return ChatResponse(
        answer=answer,
        detected_topic=topic_name,
        detected_language=detected_lang,
        difficulty_level=difficulty_level,
        within_syllabus=within_syllabus,
    )


@router.post("/voice")
async def chat_voice(request: VoiceRequest):
    """Convert text to speech and return MP3 audio."""
    audio_bytes = get_audio_bytes(request.text, request.language)
    return Response(
        content=audio_bytes,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=explanation.mp3"},
    )
