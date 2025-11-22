from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from app.scoring.pipeline_v2 import evaluate_transcript_v2

app = FastAPI(title="Communication Scoring API", version="2.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvalRequest(BaseModel):
    transcript: str
    duration_seconds: float | None = None

@app.get("/api/v2/health")
def health():
    return {"status": "ok", "version": "2.1.0"}

@app.post("/api/v2/evaluate")
def evaluate(req: EvalRequest):
    txt = req.transcript.strip()
    if not txt:
        raise HTTPException(status_code=400, detail="Transcript is empty.")
    if len(txt.split()) < 10:
        raise HTTPException(status_code=400, detail="Transcript too short for meaningful scoring (>=10 words required).")
    result = evaluate_transcript_v2(txt, req.duration_seconds)
    return result