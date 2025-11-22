# Rubric File Guide

## Using Excel (rubric.xlsx)
Columns required:
- id
- name
- description
- keywords (comma-separated)
- weight (float)
- min_words (int or blank)
- max_words (int or blank)
- enabled (TRUE/FALSE)

Example row:
intro_basics | Introduction Basics | States name and current role or field clearly at the start. | name, student, role, currently | 0.25 | 60 | 180 | TRUE

After editing Excel, either:
1. Let system parse automatically (remove rubric.json).
2. Or regenerate rubric.json via a script you create.

## Editing Weights
Ensure all weights add up logically (they do NOT need to sum to 1, code normalizes automatically).