from app.scoring.metrics import filler_words_metric

def test_filler_words_metric():
    txt = "Um well I mean like you know I like coding."
    res = filler_words_metric(txt)
    assert "filler_count" in res
    assert res["score"] in [15,12,9,6,3]