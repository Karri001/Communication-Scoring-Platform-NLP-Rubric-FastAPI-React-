import re
from typing import Optional

NAME_REGEX = re.compile(r"\bmy name is ([A-Z][a-zA-Z]*)\b", re.IGNORECASE)
GENERIC_INTRO = re.compile(r"\bmyself ([A-Z][a-zA-Z]*)\b", re.IGNORECASE)
AGE_REGEX = re.compile(r"\bI am (\d{1,2}) years? old\b", re.IGNORECASE)
CLASS_REGEX = re.compile(r"class\s+(\d{1,2}\w?)\b", re.IGNORECASE)
SCHOOL_REGEX = re.compile(r"\bfrom ([A-Z][a-zA-Z0-9\s]*(School|Academy|College))\b")

def extract_name(text: str) -> Optional[str]:
    m = NAME_REGEX.search(text)
    if m:
        return m.group(1)
    m2 = GENERIC_INTRO.search(text)
    if m2:
        return m2.group(1)
    return None

def extract_age(text: str) -> Optional[int]:
    m = AGE_REGEX.search(text)
    if m:
        return int(m.group(1))
    return None

def extract_class(text: str) -> Optional[str]:
    m = CLASS_REGEX.search(text)
    if m:
        return m.group(1)
    return None

def extract_school_class_phrase(text: str) -> Optional[str]:
    school = SCHOOL_REGEX.search(text)
    cls = CLASS_REGEX.search(text)
    parts = []
    if school:
        parts.append(school.group(1))
    if cls:
        parts.append(f"Class {cls.group(1)}")
    return ", ".join(parts) if parts else None