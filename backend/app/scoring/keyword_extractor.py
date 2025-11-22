import re
from typing import List, Tuple

def normalize(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())

def keyword_match(transcript: str, keywords: List[str]) -> Tuple[List[str], List[str]]:
    norm = normalize(transcript)
    found, missing = [], []
    for kw in keywords:
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, norm):
            found.append(kw)
        else:
            missing.append(kw)
    return found, missing

def keyword_score(found: List[str], total: int) -> float:
    if total == 0:
        return 1.0
    return len(found) / total