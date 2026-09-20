import re

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
    "i": "I",
}

def _preserve_case(original, replacement):
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement

def correct_text(text):
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

    return {
        "original_text": text,
        "corrected_text": cleaned,
        "changes": corrections,
        "change_count": len(corrections)
    }
