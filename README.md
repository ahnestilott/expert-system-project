# Laptop Expert System — Completed Mini Project

Python 3.8+ is required. No third-party dependencies.

## Run
From this folder:

```bash
python main.py
```

On systems that use `python3`, run `python3 main.py` instead.

Answer the yes/no questions to receive recommendations, specifications, and an explanation of each fired rule.

## Test
```bash
python -m unittest discover -s tests -v
```

## Contents
- `engine.py` — generic forward chaining engine with rule priorities and firing trace.
- `kb_loader.py` — original JSON rule loader.
- `kb/laptop_rules.json` — 20 laptop recommendation/specification rules.
- `main.py` — interactive questionnaire and results.
- `tests/test_expert_system.py` — automated test scenarios.
- `REPORT.md` — written explanation of the system and sample inference.

This system is educational: recommendations represent laptop categories, not specific commercial models.
