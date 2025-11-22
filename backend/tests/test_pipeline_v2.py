from app.scoring.pipeline_v2 import evaluate_transcript_v2

def test_full_pipeline():
    transcript = ("Hello everyone, my name is Arjun. I am 13 years old studying in class 8 at Riverdale School. "
                  "I love playing cricket and my dream is to become a data scientist. "
                  "A fun fact about me is that I collect old coins. Thank you.")
    result = evaluate_transcript_v2(transcript, duration_seconds=50)
    assert result.total_score <= result.max_total
    assert any(m.id == "concept" for m in result.metrics)
    assert result.extracted.name == "Arjun"