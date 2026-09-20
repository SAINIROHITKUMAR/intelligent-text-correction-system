import re
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

# Lightweight rule-based correction so the project runs without an external API key.
COMMON_CORRECTIONS = {
    "teh": "the",
    "schol": "school",
    "recieve": "receive",
    "seperate": "separate",
    "definately": "definitely",
    "occured": "occurred",
    "adress": "address",
    "becuase": "because",
    "enviroment": "environment",
    "wierd": "weird",
    "untill": "until",
    "alot": "a lot",
    "dont": "don't",
    "cant": "can't",
    "wont": "won't",
    "isnt": "isn't",
    "doesnt": "doesn't",
    "didnt": "didn't",
    "im": "I'm",
    "ive": "I've",
    "id": "I'd",
    "youre": "you're",
    "theyre": "they're",
}

LANGUAGE_TOOL_URL = "https://api.languagetool.org/v2/check"

def _preserve_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement

def _apply_language_tool(text):
    payload = urlencode({
        "text": text,
        "language": "en-US",
        "enabledOnly": "false",
    }).encode("utf-8")
    request = Request(
        LANGUAGE_TOOL_URL,
        data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "IntelligentTextCorrectionSystem/1.0"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=5) as response:
            matches = json.loads(response.read().decode("utf-8")).get("matches", [])
    except (HTTPError, URLError, TimeoutError, OSError, ValueError):
        return text, []

    changes = []
    corrected = text
    for match in sorted(matches, key=lambda item: item.get("offset", 0), reverse=True):
        replacements = match.get("replacements") or []
        offset = match.get("offset")
        length = match.get("length")
        if not replacements or not isinstance(offset, int) or not isinstance(length, int):
            continue
        replacement = replacements[0].get("value")
        if not isinstance(replacement, str):
            continue
        original = corrected[offset:offset + length]
        corrected = corrected[:offset] + replacement + corrected[offset + length:]
        changes.append({
            "original": original,
            "corrected": replacement,
            "type": "grammar/spelling",
        })
    changes.reverse()
    return corrected, changes

def correct_text(text, use_language_tool=True):
    corrections = []

    def replace(match):
        original = match.group(0)
        key = original.lower()
        if key not in COMMON_CORRECTIONS:
            return original

        replacement = _preserve_case(original, COMMON_CORRECTIONS[key])
        corrections.append({
            "original": original,
            "corrected": replacement,
            "type": "spelling/grammar"
        })
        return replacement

    corrected = re.sub(r"[A-Za-z]+(?:'[A-Za-z]+)?", replace, text)

    corrected = re.sub(
        r"(?m)(^|[.!?]\s+)i\b",
        lambda match: f"{match.group(1)}I",
        corrected
    )

    def correct_name_sentence(match):
        name = match.group(1).capitalize()
        replacement = f"My name is {name}"
        corrections.append({
            "original": match.group(0),
            "corrected": replacement,
            "type": "grammar"
        })
        return replacement

    corrected = re.sub(
        r"(?i)^\s*my\s+name?\s+([a-z]+)\s*$",
        correct_name_sentence,
        corrected
    )

    def add_missing_preposition(match):
        original = match.group(0)
        replacement = f"{original[:-6]}to school"
        corrections.append({
            "original": original,
            "corrected": replacement,
            "type": "grammar"
        })
        return replacement

    corrected = re.sub(r"\bI go school\b", add_missing_preposition, corrected, flags=re.IGNORECASE)

    # Simple punctuation cleanup.
    cleaned = re.sub(r"\s+([,.!?;:])", r"\1", corrected)
    cleaned = re.sub(r"([.!?])([A-Za-z])", r"\1 \2", cleaned)

    if use_language_tool and not corrections:
        cleaned, corrections = _apply_language_tool(cleaned)

    return {
        "original_text": text,
        "corrected_text": cleaned,
        "changes": corrections,
        "change_count": len(corrections)
    }
