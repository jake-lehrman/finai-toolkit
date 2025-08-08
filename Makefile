## Makefile for FinAI Toolkit Development
##
## This Makefile provides convenience targets for setting up the development
## environment, running tests, linting, type‑checking, and formatting.  All
## commands assume you are working inside the project root and have already
## activated the appropriate Python environment (e.g. a conda or virtualenv).

# Default target: run tests quickly
.PHONY: test
test:
	pytest -q

# Run the linter (Ruff)
.PHONY: lint
lint:
	ruff check .

# Run the type checker (Mypy)
.PHONY: type
type:
	mypy finai

# Format code with Black
.PHONY: fmt
fmt:
	black .

# Run all pre‑commit hooks on all files
.PHONY: precommit
precommit:
	pre-commit run --all-files

# Install project in editable mode and development dependencies
.PHONY: init
init:
	pip install -e .
	pip install -r requirements-dev.txt
	pre-commit install

# End‑to‑end run of tests with Python path explicitly set
.PHONY: e2e
e2e:
	PYTHONPATH=. python -m pytest -q
