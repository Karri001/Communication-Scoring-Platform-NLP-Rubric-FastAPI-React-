# Design Notes

## Objectives
- Transparent scoring
- Maintain extensibility
- Minimal cognitive load for users

## Layers
1. Data layer: rubric loader (Excel → DataFrame → Pydantic)
2. Scoring layer: modular functions (keywords, semantic, length, weighting)
3. API layer: FastAPI endpoint /score
4. Presentation: React UI, reports, export

## Decisions
- Chose FastAPI for automatic OpenAPI docs
- Chose sentence-transformers for lightweight embeddings
- Chose Tailwind for consistent design system rapid styling
- Introduced criterion-level sub-weights for tuning semantics vs keywords

## Possible Future Improvements
- Save evaluation history (SQLite)
- Add chunk-based semantic scoring (select top sentences)
- Use spaCy for advanced tokenization & lemmatization
