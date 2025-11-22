import json
from pathlib import Path
import pandas as pd
from app.models import Rubric, RubricCriterion, ScoringConfig

BASE = Path(__file__).parent.parent
RUBRIC_JSON = BASE / "rubric_samples" / "rubric.json"
RUBRIC_XLSX = BASE / "rubric_samples" / "rubric.xlsx"

def load_rubric() -> Rubric:
    if RUBRIC_JSON.exists():
        data = json.loads(RUBRIC_JSON.read_text())
        return Rubric(**data)
    if RUBRIC_XLSX.exists():
        df = pd.read_excel(RUBRIC_XLSX)
        criteria = []
        for _, row in df.iterrows():
            criteria.append(RubricCriterion(
                id=str(row['id']),
                name=str(row['name']),
                description=str(row['description']),
                keywords=[k.strip() for k in str(row['keywords']).split(',') if k.strip() != '' and not pd.isna(k)],
                weight=float(row['weight']),
                min_words=int(row['min_words']) if not pd.isna(row['min_words']) else None,
                max_words=int(row['max_words']) if not pd.isna(row['max_words']) else None,
                enabled=bool(row.get('enabled', True)),
                scoring_config=ScoringConfig()
            ))
        return Rubric(criteria=criteria)
    raise FileNotFoundError("No rubric.json or rubric.xlsx found. Provide one in rubric_samples/")