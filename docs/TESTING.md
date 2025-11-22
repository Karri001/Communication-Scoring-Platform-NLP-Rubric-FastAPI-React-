# Testing Instructions

## Unit Tests
Run:
```bash
cd backend
pytest -q
```
test_scoring.py checks:
- Pipeline returns two criterion scores
- Overall score within bounds

## Manual API Test
```bash
curl -X POST http://127.0.0.1:8000/api/v1/score \
  -H "Content-Type: application/json" \
  -d '{"transcript":"Hello my name is Alex and my future goal is to create impactful products."}'
```

Expected: JSON with overall_score, criteria array.

## Frontend Manual
1. Start backend, then `npm run dev` in frontend.
2. Paste sample transcript.
3. Click "Score".
4. Inspect network tab → 200 response.
