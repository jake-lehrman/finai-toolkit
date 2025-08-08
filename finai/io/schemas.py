"""
Data schemas for the finai toolkit.

This module defines Pydantic models representing the normalized artifacts
used throughout the library, such as filings, transcripts, chunks, events,
aligned events, labels, and evaluation results.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Filing(BaseModel):
    """Normalized representation of a filing document."""
    cik: str = Field(..., description="Central Index Key identifier for the issuer.")
    ticker: str = Field(..., description="Ticker symbol associated with the issuer.")
    filing_type: str = Field(..., description="Type of filing, e.g., 10-K, 10-Q.")
    file_time: datetime = Field(..., description="Timestamp when the filing was made public (UTC).")
    content: str = Field(..., description="Raw text content of the filing.")
    source: Optional[str] = Field(None, description="Source from which the filing was retrieved.")


class Transcript(BaseModel):
    """Normalized representation of an earnings call transcript or similar event."""
    ticker: str = Field(..., description="Ticker symbol associated with the issuer.")
    call_time: datetime = Field(..., description="Timestamp when the call started (UTC).")
    content: str = Field(..., description="Raw text content of the transcript.")
    speaker: Optional[str] = Field(None, description="Speaker name, if applicable.")
    role: Optional[str] = Field(None, description="Role of the speaker, if applicable.")


class Chunk(BaseModel):
    """Represents a deterministic chunk of text extracted from a document."""
    doc_id: str = Field(..., description="Identifier of the source document.")
    chunk_id: str = Field(..., description="Stable identifier for this chunk.")
    section_id: Optional[str] = Field(None, description="Section identifier within the document, if known.")
    text: str = Field(..., description="The content of this chunk.")
    start: int = Field(..., description="Start character offset of the chunk in the source document.")
    end: int = Field(..., description="End character offset of the chunk in the source document.")


class Event(BaseModel):
    """Structured representation of an event extracted from text."""
    event_id: str = Field(..., description="Unique identifier for the event.")
    ticker: str = Field(..., description="Ticker symbol associated with the event.")
    type: str = Field(..., description="Type of event, e.g., Guidance, Buyback.")
    announce_time: datetime = Field(..., description="When the event became public (UTC).")
    fields: Dict[str, Any] = Field(default_factory=dict, description="Event-specific fields.")


class AlignedEvent(Event):
    """Event with an associated price bar index (T0)."""
    t0: datetime = Field(..., description="Timestamp of the price bar used as T0 for alignment.")


class Label(BaseModel):
    """Target variable associated with an event and horizon."""
    event_id: str = Field(..., description="Identifier of the event this label corresponds to.")
    horizon: str = Field(..., description="Horizon for the label, e.g., '1d', '5d'.")
    value: float = Field(..., description="Numeric label value.")


class EvalResult(BaseModel):
    """Represents an evaluation metric result."""
    metric: str = Field(..., description="Name of the metric.")
    value: float = Field(..., description="Metric value.")
    details: Optional[Dict[str, Any]] = Field(None, description="Optional structured details for the metric.")


__all__ = [
    "Filing",
    "Transcript",
    "Chunk",
    "Event",
    "AlignedEvent",
    "Label",
    "EvalResult",
]
