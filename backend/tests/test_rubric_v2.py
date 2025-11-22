from app.scoring.pipeline_v2 import evaluate_transcript_v2

def test_rubric_v2_evaluation():
    transcript = ("Hello everyone, myself Muskan, studying in class 8th B section from Christ Public School. "
                  "I am 13 years old. I live with my family. There are 3 people in my family, me, my mother and my father. "
                  "One special thing about my family is that they are very kind hearted to everyone and soft spoken. "
                  "One thing I really enjoy is play, playing cricket and taking wickets. "
                  "A fun fact about me is that I see in mirror and talk by myself. "
                  "One thing people don't know about me is that I once stole a toy from one of my cousin. "
                  "My favorite subject is science because it is very interesting. Through science I can explore the whole world "
                  "and make the discoveries and improve the lives of others. Thank you for listening.")
    result = evaluate_transcript_v2(transcript, duration_seconds=52)
    assert result.total_score <= 100
    assert result.word_count > 0
    assert any(m.id == "salutation" for m in result.metrics)