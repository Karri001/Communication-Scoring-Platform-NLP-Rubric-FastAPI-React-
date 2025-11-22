import re
from typing import Dict
from language_tool_python import LanguageTool
from .constants import (
    SALUTATION_LEVELS,
    MUST_HAVE_KEYWORDS,
    GOOD_TO_HAVE_KEYWORDS,
    FILLER_WORDS
)
from .utils import word_tokens, type_token_ratio, ensure_vader
from .extraction import extract_name, extract_age, extract_class, extract_school_class_phrase

# --- Concept pattern configuration ---
MUST_HAVE_CONCEPTS = {
    "name": {
        "regex": [
            r"\bmy name is\s+[A-Z][a-zA-Z]+",
            r"\bmyself\s+[A-Z][a-zA-Z]+",
            r"\bi am\s+[A-Z][a-zA-Z]+\b"  # occasionally “I am Muskan”
        ],
        "extraction": lambda text: extract_name(text) is not None
    },
    "age": {
        "regex": [
            r"\bI am\s+\d{1,2}\s+years?\s+old\b",
            r"\bI'm\s+\d{1,2}\s+years?\s+old\b",
        ],
        "extraction": lambda text: extract_age(text) is not None
    },
    "class": {
        "regex": [
            r"\bclass\s+\d{1,2}\w?\b",
            r"\bstudying in class\s+\d{1,2}\w?\b"
        ],
        "extraction": lambda text: extract_class(text) is not None
    },
    "school": {
        "regex": [
            r"\bSchool\b",
            r"\bPublic School\b",
            r"\bHigh School\b",
            r"\bAcademy\b",
            r"\bCollege\b"
        ],
        "extraction": lambda text: extract_school_class_phrase(text) is not None
    },
    "family": {
        "regex": [
            r"\bfamily\b",
            r"\bmy (mother|father|parents|sister|brother)\b",
            r"\bthere (are|is)\s+\d+\s+people in my family\b"
        ]
    },
    "hobby": {
        "regex": [
            r"\bplaying\s+\w+",
            r"\bplay\b",
            r"\bI love\b",
            r"\bI enjoy\b",
            r"\bI really enjoy\b",
            r"\bmy favorite (subject|activity)\b",
            r"\bfavorite subject\b",
            r"\btaking wickets\b"
        ]
    },
    "interest": {
        "regex": [
            r"\bI am interested in\b",
            r"\binterested in\b",
            r"\bscience\b",  # You can narrow later
            r"\bexplore the whole world\b"
        ]
    },
    "like": {  # treat preference verbs as fulfilling “like”
        "regex": [
            r"\bI like\b",
            r"\bI love\b",
            r"\bI enjoy\b",
            r"\bfavorite\b"
        ]
    }
}

GOOD_TO_HAVE_CONCEPTS = {
    "origin": {
        "regex": [
            r"\bI am from\b",
            r"\bwe are from\b",
            r"\bmy hometown\b"
        ]
    },
    "parents are from": {
        "regex": [r"\bparents are from\b"]
    },
    "ambition": {
        "regex": [
            r"\bmy ambition\b",
            r"\bmy goal\b",
            r"\bmy dream\b",
            r"\bI aspire\b"
        ]
    },
    "goal": {
        "regex": [r"\bgoal\b"]
    },
    "dream": {
        "regex": [r"\bdream\b"]
    },
    "achievement": {
        "regex": [
            r"\bachievement\b",
            r"\bI achieved\b",
            r"\bI won\b"
        ]
    },
    "strength": {
        "regex": [
            r"\bmy strength\b",
            r"\bstrong in\b"
        ]
    },
    "fun fact": {
        "regex": [
            r"\bfun fact\b",
            r"\ba fun fact\b"
        ]
    },
    "unique": {
        "regex": [
            r"\bone special thing\b",
            r"\bsomething unique\b"
        ]
    },
    "aspire": {
        "regex": [r"\bI aspire\b"]
    },
    "interesting": {
        "regex": [
            r"\bit is very interesting\b",
            r"\binteresting\b"
        ]
    }
}

def _concept_found(text: str, concept_def: dict) -> bool:
    low = text.lower()
    # regex patterns
    for pattern in concept_def.get("regex", []):
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True
    # extraction function if present
    extractor = concept_def.get("extraction")
    if extractor and extractor(text):
        return True
    return False

def keyword_presence(text: str) -> Dict:
    must_found = []
    for concept in MUST_HAVE_CONCEPTS:
        if _concept_found(text, MUST_HAVE_CONCEPTS[concept]):
            must_found.append(concept)

    good_found = []
    for concept in GOOD_TO_HAVE_CONCEPTS:
        if _concept_found(text, GOOD_TO_HAVE_CONCEPTS[concept]):
            good_found.append(concept)

    # Each must-have concept = 4 points; each good-to-have concept = 2 points
    must_score = len(must_found) * 4
    good_score = len(good_found) * 2

    # Cap logic can be retained if desired, but original spec sets max to 30
    total_score = must_score + good_score
    if total_score > 30:
        total_score = 30  # enforce rubric maximum

    must_missing = [c for c in MUST_HAVE_CONCEPTS.keys() if c not in must_found]
    good_missing = [c for c in GOOD_TO_HAVE_CONCEPTS.keys() if c not in good_found]

    return {
        "must_found": must_found,
        "must_missing": must_missing,
        "good_found": good_found,
        "good_missing": good_missing,
        "score": total_score,
        "max": 30
    }

# ---------------- Existing functions (unchanged except import additions) ----------------
def detect_salutation(text: str) -> Dict:
    low = text.lower()
    level = "none"
    score_map = {"none": 0, "normal": 2, "good": 4, "excellent": 5}
    matched = []
    for phrase in SALUTATION_LEVELS["excellent"]:
        if phrase in low:
            level = "excellent"; matched.append(phrase); break
    if level == "none":
        for phrase in SALUTATION_LEVELS["good"]:
            if phrase in low:
                level = "good"; matched.append(phrase); break
    if level == "none":
        for phrase in SALUTATION_LEVELS["normal"]:
            if re.search(r'\b' + re.escape(phrase) + r'\b', low):
                level = "normal"; matched.append(phrase); break
    return {"level": level, "matched": matched, "score": score_map[level], "max": 5}

def flow_order(text: str) -> Dict:
    norm = text.lower()
    def first_index(candidates):
        indices = [norm.find(c) for c in candidates if norm.find(c) != -1]
        return min(indices) if indices else -1
    sal_idx = first_index(SALUTATION_LEVELS["excellent"] + SALUTATION_LEVELS["good"] + SALUTATION_LEVELS["normal"])
    basic_idx = first_index(["name", "age", "class", "school"])
    additional_idx = first_index(list(GOOD_TO_HAVE_CONCEPTS.keys()))
    closing_idx = max(norm.rfind("thank you"), norm.rfind("thanks"))
    order_components = {
        "salutation": sal_idx,
        "basic_details": basic_idx,
        "additional": additional_idx,
        "closing": closing_idx if closing_idx != -1 else -1
    }
    followed = False
    if all(v != -1 for v in order_components.values()):
        vals = list(order_components.values())
        followed = vals == sorted(vals)
    score = 5 if followed else 0
    return {"positions": order_components, "order_followed": followed, "score": score, "max": 5}

def speech_rate_metric(word_count: int, duration_seconds: float | None) -> Dict:
    if not duration_seconds or duration_seconds <= 0:
        return {"wpm": None, "band": "unknown", "score": 0, "max": 10, "note": "Duration missing"}
    wpm = word_count / (duration_seconds / 60)
    if wpm > 161: score, band = 2, "too fast"
    elif 141 <= wpm <= 160: score, band = 6, "fast"
    elif 111 <= wpm <= 140: score, band = 10, "ideal"
    elif 81 <= wpm <= 110: score, band = 6, "slow"
    else: score, band = 2, "too slow"
    return {"wpm": round(wpm,2), "band": band, "score": score, "max": 10}

def grammar_metric(text: str) -> Dict:
    words = word_tokens(text)
    wc = len(words)
    try:
        tool = LanguageTool('en-US')
        matches = tool.check(text)
    except Exception:
        return {
            "errors": 0, "errors_per_100_words": 0.0,
            "grammar_score_raw": 1.0, "band": ">0.9",
            "score": 10, "max": 10,
            "note": "LanguageTool unavailable; default high score."
        }
    def issue_type(match):
        return getattr(match, "rule_issue_type", "other")
    error_count = len([m for m in matches if issue_type(m) != 'whitespace'])
    errors_per_100 = (error_count / wc * 100) if wc else 0
    grammar_score_raw = 1 - min(errors_per_100 / 10, 1)
    if grammar_score_raw > 0.9: score, band = 10, ">0.9"
    elif grammar_score_raw >= 0.7: score, band = 8, "0.7–0.89"
    elif grammar_score_raw >= 0.5: score, band = 6, "0.5–0.69"
    elif grammar_score_raw >= 0.3: score, band = 4, "0.3–0.49"
    else: score, band = 2, "<0.3"
    return {
        "errors": error_count,
        "errors_per_100_words": round(errors_per_100,2),
        "grammar_score_raw": round(grammar_score_raw,3),
        "band": band,
        "score": score,
        "max": 10
    }

def vocabulary_metric(text: str) -> Dict:
    words = word_tokens(text)
    ttr = type_token_ratio(words)
    if ttr >= 0.9: score, band = 10, "0.9–1.0"
    elif ttr >= 0.7: score, band = 8, "0.7–0.89"
    elif ttr >= 0.5: score, band = 6, "0.5–0.69"
    elif ttr >= 0.3: score, band = 4, "0.3–0.49"
    else: score, band = 2, "0–0.29"
    return {"ttr": round(ttr,3), "band": band, "score": score, "max": 10}

def filler_words_metric(text: str) -> Dict:
    words = word_tokens(text)
    wc = len(words)
    low = text.lower()
    filler_count = 0
    for fw in FILLER_WORDS:
        filler_count += len(re.findall(r'\b' + re.escape(fw) + r'\b', low))
    rate = (filler_count / wc * 100) if wc else 0
    if rate <= 3: score, band = 15, "0–3"
    elif rate <= 6: score, band = 12, "4–6"
    elif rate <= 9: score, band = 9, "7–9"
    elif rate <= 12: score, band = 6, "10–12"
    else: score, band = 3, "13+"
    return {
        "filler_count": filler_count,
        "rate_percent": round(rate,2),
        "band": band,
        "score": score,
        "max": 15
    }

def sentiment_metric(text: str) -> Dict:
    sia = ensure_vader()
    scores = sia.polarity_scores(text)
    pos = scores.get("pos", 0.0)
    if pos >= 0.9: score, band = 15, ">=0.9"
    elif pos >= 0.7: score, band = 12, "0.7–0.89"
    elif pos >= 0.5: score, band = 9, "0.5–0.69"
    elif pos >= 0.3: score, band = 6, "0.3–0.49"
    else: score, band = 3, "<0.3"
    return {"pos_probability": round(pos,3), "band": band, "score": score, "max": 15}