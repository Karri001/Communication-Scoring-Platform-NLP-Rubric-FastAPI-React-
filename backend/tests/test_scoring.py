from app.scoring.pipeline import score_transcript
from app.models import Rubric, RubricCriterion, ScoringConfig

def test_basic_scoring():
    rubric = Rubric(criteria=[
        RubricCriterion(
            id="intro",
            name="Intro",
            description="States name and role.",
            keywords=["name", "role"],
            weight=0.5,
            scoring_config=ScoringConfig()
        ),
        RubricCriterion(
            id="goal",
            name="Goal",
            description="Mentions future aspiration.",
            keywords=["goal", "future"],
            weight=0.5,
            scoring_config=ScoringConfig()
        )
    ])
    transcript = "Hello my name is Alex and my future goal is to build helpful products in a product role."
    result = score_transcript(transcript, rubric)
    assert result.word_count > 0
    assert len(result.criteria) == 2
    assert result.overall_score <= 100