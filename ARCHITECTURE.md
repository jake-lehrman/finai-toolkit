# Architecture Overview

This document outlines the high‑level architecture of the FinAI Toolkit and explains how data flows through the system.

## Modules

### `finai/filings` and `finai/transcripts`
Provide loaders for SEC filings and earnings call transcripts. These modules handle normalization (e.g., CIK/ticker mapping), sectioning, and speaker turn identification. They also expose a deterministic chunker that splits text into token‑constrained chunks with stable `chunk_id`s.

### `finai/nlp`
Contains NLP functionality, including sentiment analysis and event extraction. It converts text chunks into **typed event objects** (e.g., buybacks, dividends, guidance revisions). Adapters for both small domain‑specific models (e.g., FinBERT) and general LLMs live here.

### `finai/align`
Responsible for mapping events onto market data bars. It handles exchange calendars, time zone normalization, and embargo logic. The core function `events_to_bars` returns an `AlignedEvent` with the aligned bar (`T0`) that is greater than or equal to the event’s `announce_time`.

### `finai/labels`
Generates target variables (labels) such as next‑day returns, cumulative abnormal returns (CARs) versus a benchmark, or changes in volatility. All labels must be computed relative to each event’s `T0` so as not to leak information.

### `finai/features`
Constructs feature matrices (X) using price data prior to T0. Example features include returns, volatility, overnight gaps, and rolling statistics. The module ensures that feature timestamps never exceed T0.

### `finai/evaluation`
Provides walk‑forward cross‑validation splitters with embargo periods to avoid leakage. Includes evaluation tools for event studies (e.g., CARs with confidence intervals), classification metrics, and transaction cost–adjusted PnL.

### `finai/io`
Defines Pydantic schemas for artifacts (`Filing`, `Transcript`, `Chunk`, `Event`, `AlignedEvent`, `Label`, `EvalResult`), as well as caching utilities and data storage helpers.

## Dataflow

1. **Ingest:** Raw filings/transcripts are loaded and normalized into structured objects.
2. **Chunk:** Deterministic chunking splits documents into token‑bounded segments.
3. **Extract:** NLP functions produce sentiment scores and typed events for each chunk.
4. **Align:** Events are mapped to market bars (T0) with calendar and embargo logic.
5. **Label & Feature:** Labels are generated relative to T0; features are built using only pre‑T0 data.
6. **Evaluate:** Walk‑forward splits, event studies, and model evaluation are performed.

## Schema Summary

See `finai/io/schemas.py` for definitions of:
* **Filing** – metadata for a filing (CIK, ticker, filing date, etc.).
* **Transcript** – metadata for a transcript (call start/end time, speakers).
* **Chunk** – a piece of text associated with a document and a stable `chunk_id`.
* **Event** – a typed event extracted from a chunk, with fields specific to the event type.
* **AlignedEvent** – an `Event` with an associated aligned bar (`T0`).
* **Label** – target variable(s) for a training example.
* **EvalResult** – container for evaluation metrics (e.g., CARs, hit ratio, Sharpe ratio).

## Key invariants

* **Point‑in‑Time safety:** All labels and features must reference data available no later than `T0`.
* **Deterministic chunking:** Same input yields same `chunk_id`s, enabling cached NLP results.
* **Embargo compliance:** For events disclosed during calls, T0 should be set after the call ends to prevent premature alignment.
* **Reproducibility:** Caching keyed on document and model identifiers prevents repeated computation and ensures reproducibility across runs.
