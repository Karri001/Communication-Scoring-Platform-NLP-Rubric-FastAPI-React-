from functools import lru_cache
from sentence_transformers import SentenceTransformer
import numpy as np

@lru_cache(maxsize=1)
def get_semantic_model():
    return SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def cosine(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-9))

CONCEPT_ANCHORS = [
    "A clear greeting",
    "States name and class or educational level",
    "Mentions school",
    "Shares family or personal background",
    "Includes hobby or interest",
    "Mentions aspiration or goal",
    "Provides unique or fun fact",
    "Polite closing thanking audience"
]

def conceptual_coverage(transcript: str) -> dict:
    """
    Computes average semantic similarity between transcript and concept anchors.
    Score bands → points (0–10):
        ≥0.80 → 10
        0.70–0.79 → 8
        0.60–0.69 → 6
        0.50–0.59 → 4
        <0.50 → 2
    """
    model = get_semantic_model()
    texts = [transcript] + CONCEPT_ANCHORS
    embeddings = model.encode(texts)
    t_embed = embeddings[0]
    sims = [cosine(t_embed, emb) for emb in embeddings[1:]]
    avg = float(np.mean(sims))
    if avg >= 0.80:
        score, band = 10, "≥0.80"
    elif avg >= 0.70:
        score, band = 8, "0.70–0.79"
    elif avg >= 0.60:
        score, band = 6, "0.60–0.69"
    elif avg >= 0.50:
        score, band = 4, "0.50–0.59"
    else:
        score, band = 2, "<0.50"
    return {
        "average_similarity": round(avg, 3),
        "individual_similarities": [round(s, 3) for s in sims],
        "anchors": CONCEPT_ANCHORS,
        "band": band,
        "score": score,
        "max": 10
    }