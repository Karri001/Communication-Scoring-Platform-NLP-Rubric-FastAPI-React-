def length_score(word_count: int, min_words, max_words) -> float:
    if not min_words and not max_words:
        return 1.0
    if min_words and word_count < min_words:
        return min(1.0, (word_count / min_words) * 0.6)
    if max_words and word_count > max_words:
        return min(1.0, (max_words / word_count) * 0.6)
    return 1.0

def combine(keyword_score, semantic_score, length_score, cfg):
    return (
        cfg.keyword_weight * keyword_score +
        cfg.semantic_weight * semantic_score +
        cfg.length_weight * length_score
    )