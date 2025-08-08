# FinAI Toolkit — Agent Brief

## Mission
Build a cohesive, LLM‑native toolkit for **financial text → events → alignment → labels → features → walk‑forward evaluation** with strong **point‑in‑time** guarantees and **leakage guards**. This brief gives agents or co‑pilots a one‑page overview of the project so they can contribute effectively.

## What exists
* Package structure: `finai/` with modules for filings, transcripts, NLP, alignment, labeling, features, evaluation and I/O utilities.
* Tooling: pytest, ruff, black, mypy, pre‑commit, GitHub Actions CI.
* Schemas: defined in `finai/io/schemas.py`.
* Sample data: located in `tests/data/`.

## Core invariants (don’t break)
* **Point‑in‑Time (PIT):** No feature or label may depend on information after the event’s alignment time (T0). All functions must enforce this.
* **Deterministic chunking:** Given the same document and chunking parameters, the chunk IDs must be stable across runs.
* **Alignment correctness:** For each event, the aligned bar (`T0`) must be greater than or equal to the event’s `announce_time` and respect any embargo period.
* **Reproducibility:** Cache keys must include `(doc_id, chunk_id, model_id, version)` to avoid re‑computing NLP results unnecessarily.

## Coding standards
* Python 3.11 with type hints; all new functions/classes must be annotated.
* Run `pre-commit install` once to enable automatic formatting and linting.
* Format code with **Black**; lint with **Ruff**; type‑check with **Mypy (strict)**.
* Prefer **Polars** over pandas for DataFrame operations unless explicit interop is needed.

## How to run locally
```
conda activate finai311
pip install -e .
pip install -r requirements-dev.txt
pytest -q
ruff check .
black --check .
mypy finai
```

## Acceptance criteria for a pull request
* New or changed APIs are documented with clear docstrings and examples.
* Unit tests and, where appropriate, golden tests are provided.
* No leakage is introduced (PIT invariants hold); add property tests if needed.
* CI passes (formatting, linting, type checking, and unit tests).
