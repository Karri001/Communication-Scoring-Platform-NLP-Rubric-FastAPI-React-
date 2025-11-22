from app.scoring.semantic import conceptual_coverage

def test_conceptual_coverage():
    text = "Hello everyone, my name is Arun. I study in class 9 at Sunrise School. I love robotics and my goal is to become an engineer. Thank you."
    result = conceptual_coverage(text)
    assert "average_similarity" in result
    assert result["score"] in [2,4,6,8,10]