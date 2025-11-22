import time
import os
from app.models import EvaluationResponse, MetricScore, ExtractedDetails
from .metrics import (
    detect_salutation,
    keyword_presence,
    flow_order,
    speech_rate_metric,
    grammar_metric,
    vocabulary_metric,
    filler_words_metric,
    sentiment_metric
)
from .extraction import (
    extract_name, extract_age,
    extract_class, extract_school_class_phrase
)
from .utils import word_tokens, sentence_split

# Simple toggle (environment variable)
ENABLE_SEMANTIC = os.getenv("ENABLE_SEMANTIC", "false").lower() == "true"

if ENABLE_SEMANTIC:
    from .semantic import conceptual_coverage  # heavy
else:
    # Lightweight stub metric
    def conceptual_coverage(transcript: str):
        return {
            "average_similarity": None,
            "individual_similarities": [],
            "anchors": [],
            "band": "disabled",
            "score": 0,
            "max": 10,
            "note": "Semantic metric disabled"
        }

def build_feedback(metric_id: str, details: dict) -> str:
    if metric_id == "salutation":
        lvl = details["level"]
        return "No greeting detected." if lvl == "none" else f"Greeting level: {lvl.capitalize()}."
    if metric_id == "keywords":
        miss = details["must_missing"]
        good_miss = details["good_missing"]
        fb = []
        if miss: fb.append(f"Missing must-have: {', '.join(miss)}.")
        if good_miss: fb.append(f"Could add: {', '.join(good_miss)}.")
        if not fb: fb.append("All key elements present.")
        return " ".join(fb)
    if metric_id == "flow":
        return "Logical order followed." if details["order_followed"] else "Improve order: greeting → basics → additional → closing."
    if metric_id == "speech_rate":
        if details["wpm"] is None: return "Provide duration for speech rate scoring."
        return f"WPM {details['wpm']} classified as {details['band']}."
    if metric_id == "grammar":
        return f"Grammar band {details['band']} with {details['errors']} errors."
    if metric_id == "vocabulary":
        return f"TTR {details['ttr']} ({details['band']})."
    if metric_id == "clarity":
        return f"Filler rate {details['rate_percent']}% ({details['band']})."
    if metric_id == "engagement":
        return f"Positive sentiment {details['pos_probability']} ({details['band']})."
    if metric_id == "concept":
        if details.get("band") == "disabled":
            return "Semantic coverage disabled."
        return f"Conceptual coverage {details['average_similarity']} ({details['band']})."
    return ""

def evaluate_transcript_v2(transcript: str, duration_seconds: float | None = None) -> EvaluationResponse:
    start = time.time()
    words = word_tokens(transcript)
    sentences = sentence_split(transcript)
    wc = len(words)
    sc = len(sentences)
    preview = transcript[:240] + ("..." if len(transcript) > 240 else "")

    sal = detect_salutation(transcript)
    kw = keyword_presence(transcript)
    fl = flow_order(transcript)
    sr = speech_rate_metric(wc, duration_seconds)
    gr = grammar_metric(transcript)
    vb = vocabulary_metric(transcript)
    clr = filler_words_metric(transcript)
    sg = sentiment_metric(transcript)
    cc = conceptual_coverage(transcript)

    metrics = [
        MetricScore(id="salutation", name="Salutation Level", raw_score=sal["score"], max_score=sal["max"], details=sal, feedback=build_feedback("salutation", sal)),
        MetricScore(id="keywords", name="Keyword Presence", raw_score=kw["score"], max_score=kw["max"], details=kw, feedback=build_feedback("keywords", kw)),
        MetricScore(id="flow", name="Flow Order", raw_score=fl["score"], max_score=fl["max"], details=fl, feedback=build_feedback("flow", fl)),
        MetricScore(id="speech_rate", name="Speech Rate (WPM)", raw_score=sr["score"], max_score=sr["max"], details=sr, feedback=build_feedback("speech_rate", sr)),
        MetricScore(id="grammar", name="Grammar Quality", raw_score=gr["score"], max_score=gr["max"], details=gr, feedback=build_feedback("grammar", gr)),
        MetricScore(id="vocabulary", name="Vocabulary Richness (TTR)", raw_score=vb["score"], max_score=vb["max"], details=vb, feedback=build_feedback("vocabulary", vb)),
        MetricScore(id="clarity", name="Clarity (Filler Rate)", raw_score=clr["score"], max_score=clr["max"], details=clr, feedback=build_feedback("clarity", clr)),
        MetricScore(id="engagement", name="Engagement (Sentiment)", raw_score=sg["score"], max_score=sg["max"], details=sg, feedback=build_feedback("engagement", sg)),
        MetricScore(id="concept", name="Conceptual Coverage", raw_score=cc["score"], max_score=cc["max"], details=cc, feedback=build_feedback("concept", cc)),
    ]

    total = sum(m.raw_score for m in metrics)

    from .extraction import extract_name, extract_age, extract_class, extract_school_class_phrase
    name = extract_name(transcript)
    age = extract_age(transcript)
    cls = extract_class(transcript)
    school_phrase = extract_school_class_phrase(transcript)
    extracted = ExtractedDetails(
        name=name,
        age=age,
        school_class=school_phrase or (f"Class {cls}" if cls else None)
    )
    perf_ms = int((time.time() - start) * 1000)

    # Adjust max_total when semantic disabled
    max_total = 110 if ENABLE_SEMANTIC else 100

    return EvaluationResponse(
        total_score=round(total, 2),
        max_total=max_total,
        word_count=wc,
        sentence_count=sc,
        duration_seconds=duration_seconds,
        wpm=sr.get("wpm"),
        metrics=metrics,
        extracted=extracted,
        transcript_preview=preview,
        version="2.1.1" if ENABLE_SEMANTIC else "2.1.1-lite",
        performance_ms=perf_ms,
        notes="Semantic disabled" if not ENABLE_SEMANTIC else "Full metric set"
    )
