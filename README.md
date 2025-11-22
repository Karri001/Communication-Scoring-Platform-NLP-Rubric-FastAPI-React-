# Communication Scoring Platform (FastAPI + React)

> Version: 2.1.1 (lite mode if semantic disabled)

An end‑to‑end platform that evaluates student self‑introduction transcripts using a transparent, rubric‑based NLP scoring engine. It provides structured feedback across greeting quality, content coverage, flow, clarity, sentiment, grammar, and optional semantic conceptual coverage.

---

## 1. Key Features

- FastAPI backend with modular metric pipeline
- React + Vite + Tailwind frontend (dark/light theme)
- Rich, explainable metrics (each with details + feedback)
- Concept-based keyword detection (not just literal tokens)
- Grammar evaluation (LanguageTool) with fallback
- Sentiment (VADER) scoring
- Filler word rate & speech rate (WPM)
- Vocabulary richness (Type–Token Ratio)
- Optional semantic conceptual coverage (Sentence-Transformers)
- Extracted fields: name, age, class/school phrase
- Toggle semantic metric via environment variable (ENABLE_SEMANTIC)
- Performance timing (ms) included in responses

---

## 2. Architecture (High-Level)

```
frontend (React/Vite/Tailwind)
    ├─ Input form (transcript + duration)
    ├─ Calls /api/v2/evaluate
    └─ Displays metric cards + extracted entities

backend (FastAPI)
    ├─ main.py (routes, CORS, health)
    ├─ scoring/
    │    ├─ metrics.py (core rule-based metrics)
    │    ├─ extraction.py (name, age, class)
    │    ├─ semantic.py (heavy semantic model; optional)
    │    ├─ pipeline_v2.py (orchestrates all metrics)
    │    ├─ utils.py (tokenization helpers)
    │    └─ constants.py (keyword lists)
    ├─ models.py (Pydantic response models)
    └─ tests/ (per-metric + pipeline tests)
```

---

## 3. Rubric (v2.1)

| Metric | Max Points | Description / Band Logic |
|--------|------------|---------------------------|
| Salutation Level | 5 | none=0, normal=2, good=4, excellent=5 (pattern-based) |
| Keyword Presence (Concepts) | 30 | Must-have concepts (8 × 4 = 32 capped) + good-to-have concepts (2 pts each) → capped at 30 |
| Flow Order | 5 | Greeting → basic details → additional info → closing (exact sequence) |
| Speech Rate (WPM) | 10 | 111–140 ideal=10; 141–160 fast=6; 81–110 slow=6; extremes=2; no duration=0 |
| Grammar Quality | 10 | Error-normalized score mapped to bands (10 / 8 / 6 / 4 / 2) |
| Vocabulary Richness (TTR) | 10 | TTR bands: ≥0.9=10; 0.7–0.89=8; 0.5–0.69=6; 0.3–0.49=4; <0.3=2 |
| Clarity (Filler Rate) | 15 | Percent fillers: 0–3%=15; 4–6%=12; 7–9%=9; 10–12%=6; ≥13%=3 |
| Engagement (Sentiment) | 15 | Positive sentiment probability: ≥0.9=15; 0.7–0.89=12; 0.5–0.69=9; 0.3–0.49=6; <0.3=3 |
| Conceptual Coverage (Semantic) | 10 | Requires ENABLE_SEMANTIC=true (sentence-transformers similarity) |
| TOTAL (Full) | 110 | Semantic enabled |
| TOTAL (Lite) | 100 | Semantic disabled (concept metric score=0) |

---

## 4. Installation & Local Development

### Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\Activate.ps1
source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('vader_lexicon')"
# Optional: export ENABLE_SEMANTIC=true
uvicorn app.main:app --reload
```

Health check: http://127.0.0.1:8000/api/v2/health

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend dev URL: http://localhost:5173

Create `frontend/.env` for local overrides:
```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

---

## 5. Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| ENABLE_SEMANTIC | false | If true, loads sentence-transformers for conceptual coverage |
| (Frontend) VITE_API_BASE_URL | required | Base URL of deployed backend (without trailing slash) |

---

## 6. API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | / | Root info (optional if added) |
| GET | /api/v2/health | Status/version check |
| GET | /api/v2/ping | Timestamp ping (optional) |
| POST | /api/v2/evaluate | Evaluate transcript JSON |

### POST /api/v2/evaluate Request JSON

```json
{
  "transcript": "Hello everyone, my name is Arjun. I am 13 years old studying in class 8 at Riverdale School. I love playing cricket. Thank you.",
  "duration_seconds": 55
}
```

### Response (Lite Example)

```json
{
  "total_score": 82.0,
  "max_total": 100,
  "word_count": 44,
  "sentence_count": 5,
  "duration_seconds": 55.0,
  "wpm": 48.0,
  "metrics": [
    {
      "id": "keywords",
      "name": "Keyword Presence",
      "raw_score": 30,
      "max_score": 30,
      "details": {
        "must_found": ["name","age","class","school","family","hobby","interest","like"],
        "must_missing": [],
        "good_found": ["fun fact"],
        "good_missing": ["origin","ambition", "..."],
        "score": 30,
        "max": 30
      },
      "feedback": "All key elements present."
    }
  ],
  "extracted": {
    "name": "Arjun",
    "age": 13,
    "school_class": "Riverdale School, Class 8"
  },
  "transcript_preview": "Hello everyone, my name is Arjun. I am 13 years old studying in class 8 at Riverdale School. I love playing cricket. Thank you.",
  "version": "2.1.1-lite",
  "performance_ms": 412,
  "notes": "Semantic disabled"
}
```

---

## 7. Semantic Metric (Optional)

To enable conceptual coverage:
1. Add back heavy dependency in `backend/requirements.txt`:
   ```
   sentence-transformers
   ```
2. Set environment variable:
   ```
   ENABLE_SEMANTIC=true
   ```
3. Redeploy backend (first request will download model; may take 20–40s).
4. Response `version` becomes `2.1.1`.

If memory constrained (e.g., free hosting) keep it disabled.

---

## 8. Deployment

### Backend (Render)

- Root directory: `backend`
- Build command:
  ```
  pip install -r requirements.txt && python -c "import nltk; nltk.download('vader_lexicon')"
  ```
- Start command:
  ```
  uvicorn app.main:app --host 0.0.0.0 --port $PORT
  ```
- Env var (optional): ENABLE_SEMANTIC=false (recommended for free tier)

### Frontend (Vercel)

- Root: `frontend`
- Build: `npm run build`
- Output: `dist`
- Env: `VITE_API_BASE_URL=https://<your-backend-domain>`

### CORS Hardening

In `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 9. Testing

Run backend tests:
```bash
cd backend
pytest -q
```

Recommended test categories:
- Grammar metric
- Filler words metric
- Sentiment metric
- Vocabulary metric
- Extraction (name/age/class)
- Pipeline integration

---

## 10. Development Workflow

1. Branch naming: `feature/<short-desc>` or `fix/<issue-number>`
2. Add tests for new metrics before merging.
3. Run formatter:
   - Python: `black .`
   - JS/TS: `npx prettier --write .`
4. Commit small, focused changes.

---

## 11. Extensibility Ideas

| Feature | Approach |
|---------|----------|
| Audio pause analysis | Integrate WebRTC or upload & run simple energy/pause extraction |
| PDF report export | Use WeasyPrint / ReportLab with HTML template |
| History tracking | Add SQLite + user session id |
| Multi-language grammar | Switch LanguageTool language codes |
| NER-based keyword scoring | spaCy for robust person/place detection |

---

## 12. Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| 400 Transcript too short | <10 words | Provide longer sample |
| Generic "Error" toast | Backend 500 / network mismatch | Check Network tab & backend logs |
| CORS error in console | Origin not allowed | Add frontend domain to allow_origins |
| Very slow first request | Model/JAR cold start | Trigger warm-up endpoint or disable semantic |
| Memory restart on free tier | Heavy torch dependencies | Disable semantic or use lighter TF-IDF |

---

## 13. Warm-Up Endpoint (Optional)

Add in `main.py`:
```python
from fastapi import BackgroundTasks
@app.get("/api/v2/warmup")
def warmup(bg: BackgroundTasks):
    def _load():
        if os.getenv("ENABLE_SEMANTIC","false").lower() == "true":
            from app.scoring.semantic import get_semantic_model
            get_semantic_model()
        from language_tool_python import LanguageTool
        LanguageTool('en-US')
    bg.add_task(_load)
    return {"status": "warming"}
```

---

## 14. Roadmap

- Phase 1: Transcript scoring (DONE)
- Phase 2: Lightweight semantic or TF-IDF conceptual hints (optional)
- Phase 3: Audio timing + pause metrics
- Phase 4: Instructor dashboard & batch analytics
- Phase 5: Multi-language support + adaptive feedback
- Phase 6: Export / integration (PDF, LMS connectors)

---

## 15. License

MIT License (see `LICENSE`).

---

## 16. Contributing

See `CONTRIBUTING.md` for:
- Setup instructions
- Branching
- Code style
- Pull request checklist

---

## 17. Internship / Portfolio Pitch

This project demonstrates full-stack implementation with explainable NLP metrics: rule-based decomposition, modular pipeline design, semantic extensibility, and a modern UI. It shows proficiency in Python, FastAPI, React, and practical NLP integration under deployment constraints.

---

## 18. Acknowledgments

- LanguageTool for grammar analysis
- NLTK VADER for sentiment
- Sentence-Transformers (optional) for semantic coverage inspiration

---

## 19. Example Quick Start (All-in-One)

```bash
# Backend (lite)
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('vader_lexicon')"
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Frontend
cd ../frontend
echo "VITE_API_BASE_URL=http://127.0.0.1:8000" > .env
npm install
npm run dev
```

Open http://localhost:5173 and score a transcript.

---

**Hosted Frontend:** https://communication-scoring-platform-nlp-rubric-fast-api-ot0ra8fqb.vercel.app
