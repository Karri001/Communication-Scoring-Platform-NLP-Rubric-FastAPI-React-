from app.scoring.metrics import sentiment_metric

def test_sentiment_metric():
    txt = "I am excited and grateful for this opportunity. Thank you everyone."
    res = sentiment_metric(txt)
    assert "pos_probability" in res
    assert res["score"] in [3,6,9,12,15]