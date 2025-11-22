def build_feedback(found, missing, semantic_score, length_score, min_words, max_words, word_count):
    parts = []
    if found:
        parts.append(f"Found: {', '.join(found)}.")
    if missing:
        parts.append(f"Missing: {', '.join(missing)}.")
    if semantic_score >= 0.8:
        parts.append("Strong alignment.")
    elif semantic_score >= 0.6:
        parts.append("Moderate alignment; consider refining phrasing.")
    else:
        parts.append("Low alignment; expand or clarify content.")
    if min_words and word_count < min_words:
        parts.append(f"Below minimum ({word_count}/{min_words}). Add detail.")
    if max_words and word_count > max_words:
        parts.append(f"Above maximum ({word_count}/{max_words}). Tighten wording.")
    return " ".join(parts)