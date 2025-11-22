from app.scoring.metrics import vocabulary_metric

def test_vocab_metric():
    txt = "innovation innovation innovation creativity design learning progress"
    res = vocabulary_metric(txt)
    assert "ttr" in res
    assert res["score"] in [2,4,6,8,10]