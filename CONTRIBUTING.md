# Contributing Guide

Thank you for considering contributing to the FinAI Toolkit! This guide outlines how to get your development environment set up, coding standards to follow, and how to propose changes.

## Getting Started

1. **Create and activate the development environment**
   ```bash
   conda create -n finai311 python=3.11 -y
   conda activate finai311
   ```
2. **Install the project in editable mode and development dependencies**
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```
3. **Install pre‑commit hooks (run once)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Style & Quality

* **Formatting:** Code must be formatted with [Black](https://black.readthedocs.io/). Pre‑commit will run Black automatically before each commit.
* **Linting:** We use [Ruff](https://docs.astral.sh/ruff/) for linting. Address any reported issues before submitting a pull request.
* **Typing:** Type hints are mandatory. Run `mypy --strict finai` to ensure type correctness.
* **Imports & Dependencies:** Use standard library modules when possible; minimize additional dependencies. Prefer Polars for DataFrame operations unless compatibility with pandas is required.

## Tests

* Put test modules in the `tests/` directory, mirroring the package structure.
* For deterministic outputs (e.g., chunk IDs, cached NLP results), add **golden tests** that write expected outputs to JSONL or Parquet. See existing tests for examples.
* To guarantee point‑in‑time safety and alignment correctness, add **property tests** (Hypothesis) to check invariants across random inputs.
* Run the full test suite with `pytest -q` and ensure it passes before committing.

## Pull Request Checklist

Before opening a pull request, please ensure:

* [ ] New or modified APIs have docstrings explaining arguments, return values, and examples if applicable.
* [ ] Unit tests cover new functionality; golden tests updated if output changed intentionally.
* [ ] No point‑in‑time leakage is introduced (verified with property tests and careful review).
* [ ] `pre-commit` passes (formatting, linting, type checks) and CI is green.
* [ ] Documentation (`docs/`, `AGENT_BRIEF.md`, `ARCHITECTURE.md`, etc.) updated as needed.

## How to Propose a Feature or Fix

1. **Open an issue** describing the change, referencing any related existing issues or pull requests.
2. **Discuss** the proposal with maintainers and gather feedback.
3. **Fork the repository** and create a feature branch from `main`.
4. **Implement** the change following the guidelines above.
5. **Open a pull request**, filling out the provided template (if available) and linking the issue.

Thank you for helping make FinAI better!
