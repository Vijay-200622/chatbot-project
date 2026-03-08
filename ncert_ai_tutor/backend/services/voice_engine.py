"""Voice engine — text-to-speech using gTTS."""

import tempfile
import re
from pathlib import Path
from gtts import gTTS


def detect_language_for_tts(text: str) -> str:
    """Detect if text is Tanglish (Tamil-heavy) or Hinglish (Hindi-heavy).

    Returns gTTS language code: 'hi' for Hindi/Hinglish, 'ta' for Tamil/Tanglish, 'en' for English.
    """
    # Tamil Unicode range: \u0B80-\u0BFF
    tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", text))
    # Devanagari Unicode range: \u0900-\u097F
    hindi_chars = len(re.findall(r"[\u0900-\u097F]", text))

    total = len(text)
    if total == 0:
        return "en"

    if tamil_chars > hindi_chars and tamil_chars > 0:
        return "ta"
    elif hindi_chars > 0:
        return "hi"
    return "hi"  # Default to Hindi for Hinglish (romanized)


def text_to_speech(text: str, lang: str = None) -> str:
    """Convert text to speech and save as MP3.

    Returns the path to the generated MP3 file.
    """
    if lang is None:
        lang = detect_language_for_tts(text)

    # Clean text for TTS (remove markdown formatting)
    clean_text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    clean_text = re.sub(r"[#*_`]", "", clean_text)
    clean_text = clean_text.strip()

    if not clean_text:
        clean_text = "Koi response nahi mila."

    try:
        tts = gTTS(text=clean_text, lang=lang, slow=False)
    except Exception:
        # Fallback to English if language not supported
        tts = gTTS(text=clean_text, lang="en", slow=False)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(tmp.name)
    return tmp.name


def get_audio_bytes(text: str, lang: str = None) -> bytes:
    """Convert text to speech and return MP3 bytes."""
    file_path = text_to_speech(text, lang)
    audio_bytes = Path(file_path).read_bytes()
    # Clean up temp file
    try:
        Path(file_path).unlink()
    except OSError:
        pass
    return audio_bytes
