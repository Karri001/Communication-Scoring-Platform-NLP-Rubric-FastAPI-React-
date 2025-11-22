from typing import List
from app.models import Rubric, ScoreResponse, CriterionScore
from .keyword_extractor import keyword_match, keyword_score
from .semantic import semantic_similarity, band
from .weighting import length_score, combine
from .feedback import build_feedback

def score_transcript(transcript: str, rubric: Rubric) -> ScoreResponse:
    word_count = len(transcript.split())
    criterion_scores: List[CriterionScore] = []
    total_weighted = 0.0
    active_weight_sum = 0.0

    for c in rubric.criteria:
        if not c.enabled:
            continue
        found, missing = keyword_match(transcript, c.keywords)
        k_score = keyword_score(found, len(c.keywords))
        s_score = semantic_similarity(transcript, c.description)
        l_score = length_score(word_count, c.min_words, c.max_words)
        combined = combine(k_score, s_score, l_score, c.scoring_config)
        weighted = combined * c.weight
        alignment_band = band(s_score)
        feedback = build_feedback(found, missing, s_score, l_score,
                                  c.min_words, c.max_words, word_count)

        criterion_scores.append(CriterionScore(
            id=c.id,
            name=c.name,
            weight=c.weight,
            keyword_score=round(k_score, 3),
            semantic_score=round(s_score, 3),
            length_score=round(l_score, 3),
            combined_score=round(combined, 3),
            weighted_score=round(weighted, 3),
            keywords_found=found,
            keywords_missing=missing,
            feedback=feedback,
            alignment_band=alignment_band
        ))
        total_weighted += weighted
        active_weight_sum += c.weight

    overall = (total_weighted / active_weight_sum) * 100 if active_weight_sum > 0 else 0.0
    preview = transcript[:240] + ("..." if len(transcript) > 240 else "")
    return ScoreResponse(
        overall_score=round(overall, 2),
        word_count=word_count,
        criteria=criterion_scores,
        transcript_preview=preview
    )