import re
import nltk

def sentence_split(text: str) -> list:
    # Simple sentence split (avoid heavy deps)
    return [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]

def normalize(text: str) -> str:
    return re.sub(r'[^a-zA-Z0-9\s]', ' ', text.lower())

def word_tokens(text: str) -> list:
    return [w for w in normalize(text).split() if w]

def type_token_ratio(words: list) -> float:
    if not words:
        return 0.0
    distinct = len(set(words))
    return distinct / len(words)

def ensure_vader():
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer()
    except LookupError:
        nltk.download('vader_lexicon')
        from nltk.sentiment import SentimentIntensityAnalyzer
        return SentimentIntensityAnalyzer()