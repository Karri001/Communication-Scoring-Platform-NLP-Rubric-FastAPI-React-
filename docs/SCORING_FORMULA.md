# Scoring Formula (Detailed)

Let criteria set = C.

For criterion i:

Raw components:
- Keyword score: K_i = matched / total (if total=0 ⇒ 1)
- Semantic score: M_i = cosine(embedding(transcript), embedding(description))
- Length score: 
  - If no bounds ⇒ L_i = 1
  - If words < min ⇒ L_i = (words / min) * 0.6
  - If words > max ⇒ L_i = (max / words) * 0.6
  - Else ⇒ L_i = 1

Combined per-criterion:
S_i = w_kw_i * K_i + w_sem_i * M_i + w_len_i * L_i

Weighted:
W_i = S_i * α_i (α_i = rubric weight)

Overall:
Overall = (Σ_i W_i / Σ_i α_i) * 100

Rationale:
- Keywords ensure explicit content coverage.
- Semantic similarity captures conceptual alignment beyond exact matches.
- Length enforces discipline and expected verbosity.
- Weights allow rubric importance prioritization.

Normalization:
All component scores ∈ [0,1], ensuring fairness when aggregated.
