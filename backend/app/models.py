from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class MetricScore(BaseModel):
    id: str
    name: str
    raw_score: float
    max_score: float
    details: Dict[str, Any]
    feedback: str

class ExtractedDetails(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    school_class: Optional[str] = None

class EvaluationResponse(BaseModel):
    total_score: float
    max_total: float
    word_count: int
    sentence_count: int
    duration_seconds: Optional[float]
    wpm: Optional[float]
    metrics: List[MetricScore]
    extracted: ExtractedDetails
    transcript_preview: str
    version: str = "2.1.0"
    performance_ms: Optional[int] = None
    notes: Optional[str] = None