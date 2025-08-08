# Roadmap

This document outlines the phased development plan for the **FinAI Toolkit** MVP.  The roadmap is designed for someone working on the project part time (around 10 – 12 hours per week) and emphasises shipping vertical slices of functionality at the end of each week.  Each milestone builds on the previous week’s work and delivers something usable and testable.

## Weeks 1–2: Foundations

- **Data Schemas**: Implement Pydantic models for all core data objects (`Filing`, `Transcript`, `Chunk`, `Event`, `AlignedEvent`, `Label`, `EvalResult`).  Establish consistent field naming, types, and docstrings.  Round‑trip conversions to and from JSON should be tested.
- **Repo Hygiene**: Set up `pytest`, `ruff`, `black`, `mypy` and pre‑commit hooks.  Configure CI to run tests and lint checks automatically.  Add a minimal `mkdocs.yml` for future documentation.
- **Tiny Gold Dataset**: Add a small set of sample filings, transcripts, and price data under `tests/data/` for golden tests.  These fixtures allow deterministic testing of parsing and alignment routines.

## Weeks 3–4: Chunking and NLP v1

- **Deterministic Chunking**: Implement section‑aware, token‑budget chunking for filings and transcripts.  Each `chunk_id` should be stable given the same input so that cached NLP results can be reused.
- **Cache Backend**: Create a simple file‑system cache keyed by `(doc_id, chunk_id, model_id, version)` to avoid repeated NLP calls on unchanged text.  Provide an interface to swap out caching backends in the future.
- **Basic NLP Extraction**:
  - **Sentiment**: Integrate a lightweight FinBERT‑style model to compute sentiment on each chunk.  Aggregate sentiments at the section level for filings.
  - **Event Extraction v1**: Use rule‑based approaches (regexes combined with NER) to detect common corporate actions such as guidance changes, share repurchases, and dividend announcements.  Emit typed `Event` objects with fields like `metric`, `amount`, `old_value`, and `new_value`.

## Weeks 5–6: Alignment, Labels and Features

- **Event → Bar Alignment**: Implement utilities for mapping event timestamps to the correct price bars.  Support exchange calendars (e.g. NYSE), time‑zone handling, and embargo windows (e.g. wait until an earnings call ends before aligning).  Ensure aligned `T0` is always at or after the `announce_time`.
- **Labels**: Provide helpers for generating target variables.  Examples include next‑day and 5‑day returns, cumulative abnormal returns (CARs) relative to a benchmark, and volatility jumps.  All labels must be computed relative to `T0` to avoid look‑ahead bias.
- **Features**: Implement a small set of features such as daily and multi‑day returns, realised volatility, overnight gaps, and rolling means.  Feature timestamps must be strictly less than or equal to `T0`.

## Week 7: Walk‑Forward Splits and Evaluation

- **Walk‑Forward Splitters**: Create time‑ordered train/test splitters with purge and embargo logic to prevent leakage.  Support expanding and rolling window schemes as well as grouping by asset.
- **Evaluation**: Build an event‑study evaluator that computes CARs with confidence intervals, hit ratios for classification tasks, and PnL with turnover/transaction‑cost adjustments.  Visualise results with simple plots.
- **Notebook A**: Produce a polished notebook demonstrating the pipeline on an earnings guidance example, from loading the call transcript to running an event study.

## Week 8: Notebook B, Docs and Release

- **Notebook B**: Create a second example that analyses sentiment shifts in 10‑K filings and measures post‑filing drift.  Use the full pipeline and illustrate how to interpret results.
- **Documentation**: Write a quick‑start guide, an API reference for each module, and a leakage checklist.  Publish the docs using MkDocs.
- **Release v0.1.0**: Tag the first version on PyPI.  Announce the project on social media and invite feedback.

## Post‑MVP: Future Enhancements

- **Enhanced Extraction**: Add more sophisticated NER models and incorporate small open‑source LLMs for better event detection and classification.  Support additional corporate actions like mergers, IPOs, and management changes.
- **Dataset Connectors**: Provide built‑in connectors to popular market data providers (e.g., Polygon.io, Yahoo Finance) and point‑in‑time fundamentals.  Consider a dataset registry with versioning.
- **Hosted API**: Offer a hosted service that performs extraction, alignment, and evaluation on user‑supplied documents via a simple API.  Provide paid tiers with higher throughput and additional models.
- **Community Involvement**: Encourage external contributions, add governance docs, and build a template repository for downstream projects.
