"""
Optional helper: regenerate rubric.json from rubric.xlsx
Usage:
    python scripts/parse_rubric.py
"""
import pandas as pd
import json
from pathlib import Path

backend_dir = Path(__file__).parent.parent / "backend"
xlsx = backend_dir / "rubric_samples" / "rubric.xlsx"
out = backend_dir / "rubric_samples" / "rubric.json"

df = pd.read_excel(xlsx)
criteria = []
for _, row in df.iterrows():
    criteria.append({
        "id": str(row['id']),
        "name": str(row['name']),
        "description": str(row['description']),
        "keywords": [k.strip() for k in str(row['keywords']).split(',') if k.strip()],
        "weight": float(row['weight']),
        "min_words": int(row['min_words']) if not pd.isna(row['min_words']) else 0,
        "max_words": int(row['max_words']) if not pd.isna(row['max_words']) else 0,
        "enabled": True,
        "scoring_config": {
            "keyword_weight": 0.4,
            "semantic_weight": 0.4,
            "length_weight": 0.2
        }
    })
rubric = {"criteria": criteria}
out.write_text(json.dumps(rubric, indent=2))
print(f"Written: {out}")