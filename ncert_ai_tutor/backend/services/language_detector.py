"""Detect input language style: Tanglish, Hinglish, or English.

Uses romanized keyword heuristics since students type in Latin script.
"""

import re

# Common Tanglish (Tamil+English) markers — romanized Tamil words
_TANGLISH_MARKERS = {
    # question words / connectors
    "enna", "ennanga", "epdi", "epdinga", "yenna", "yaar", "yaaru",
    "ethuku", "ethu", "eppadi", "eppdi", "enga", "engal",
    # verbs / phrases
    "sollu", "sollunge", "solunga", "panni", "pannunga", "pannu",
    "puriyala", "puriyathu", "purinjuchu", "puringiducha", "puriyudhu",
    "theriyala", "theriyum", "theriyathu", "therinja",
    "paaru", "paarunga", "pathu", "paadam",
    "kandu", "kandupidi", "sonna", "sonnen",
    "konjam", "konjum", "nalla", "nalladhu",
    "vaanga", "vaa", "vandhiruchu",
    "iruku", "irukku", "illa", "illai",
    "romba", "oru", "innoru", "antha", "ithu", "athu",
    "thaan", "thanga", "ungaluku", "enaku", "enakku", "unaku",
    "padi", "padinga", "padikanum",
    # pronouns / address
    "nee", "neenga", "naan", "naanga",
    "anna", "akka", "thala",
    # subject-specific
    "pathi", "pathii", "patri", "patriya",
    # copula / aux
    "da", "di", "la", "le", "nu", "um",
    "aana", "aanaa", "aanalum",
}

# Common Hinglish (Hindi+English) markers — romanized Hindi words
_HINGLISH_MARKERS = {
    # question words / connectors
    "kya", "kaise", "kyun", "kab", "kahan", "kaun", "kitna", "kitne",
    "kisko", "kis",
    # verbs / phrases
    "samjha", "samjhao", "samjhana", "samajh", "samjho",
    "batao", "bataao", "batana", "bata",
    "karo", "karna", "karein", "karte",
    "hai", "hain", "tha", "the", "hota", "hoti",
    "nahi", "nai", "nahin",
    "mein", "meri", "mera", "mere",
    "kuch", "bahut", "bohot", "thoda", "zyada", "sabse",
    "dekh", "dekho", "dekhna",
    "padh", "padho", "padhna", "padhao",
    "yaar", "bhai", "bhaiya", "didi",
    "acha", "achha", "achhi", "accha",
    "wala", "wali", "wale",
    "aur", "ya", "lekin", "par", "ki", "ka", "ke", "ko", "se", "ne",
    "toh", "to", "tab",
    # pronouns / address
    "mujhe", "mujhko", "tujhe", "humko", "unko", "hamein",
    "hum", "tum", "aap",
    # subject-specific
    "matlab",
    # common phrases
    "arrey", "arey", "arre", "pehle", "phir",
    "do", "de", "dena", "dedo", "dijiye",
    "madat", "madad",
}


def detect_input_language(text: str) -> str:
    """Detect whether input is Tanglish, Hinglish, or English.

    Also checks for explicit language requests like "explain in English",
    "in Tamil", "in Hindi" etc.

    Returns one of: 'tanglish', 'hinglish', 'english'
    """
    text_lower = text.lower()

    # 1. Check for EXPLICIT language requests first (highest priority)
    _english_request = re.search(
        r'\b(in\s+english|english\s+me|english\s+mein|english\s+la|reply\s+in\s+english|answer\s+in\s+english|explain\s+in\s+english|tell\s+in\s+english|convert\s+to\s+english)\b',
        text_lower,
    )
    if _english_request:
        return "english"

    _tamil_request = re.search(
        r'\b(in\s+tamil|tamil\s+la|tamil\s+le|tanglish\s+la|tanglish\s+le|reply\s+in\s+tamil|answer\s+in\s+tamil|explain\s+in\s+tamil)\b',
        text_lower,
    )
    if _tamil_request:
        return "tanglish"

    _hindi_request = re.search(
        r'\b(in\s+hindi|hindi\s+me|hindi\s+mein|hinglish\s+me|hinglish\s+mein|reply\s+in\s+hindi|answer\s+in\s+hindi|explain\s+in\s+hindi)\b',
        text_lower,
    )
    if _hindi_request:
        return "hinglish"

    # 2. Keyword-based detection
    words = set(re.findall(r"[a-zA-Z]+", text_lower))

    tanglish_score = sum(1 for w in words if w in _TANGLISH_MARKERS)
    hinglish_score = sum(1 for w in words if w in _HINGLISH_MARKERS)

    # Check for Tamil Unicode chars as well
    tamil_chars = len(re.findall(r"[\u0B80-\u0BFF]", text))
    hindi_chars = len(re.findall(r"[\u0900-\u097F]", text))

    tanglish_score += min(tamil_chars, 5)
    hinglish_score += min(hindi_chars, 5)

    if tanglish_score == 0 and hinglish_score == 0:
        return "english"

    if tanglish_score > hinglish_score:
        return "tanglish"
    elif hinglish_score > tanglish_score:
        return "hinglish"
    else:
        # Tie: check for strong Tamil markers
        strong_tamil = {"anna", "akka", "pathi", "pathii", "sollu", "paaru",
                        "puriyala", "konjam", "nee", "neenga", "romba", "da", "la"}
        if words & strong_tamil:
            return "tanglish"
        return "hinglish"
