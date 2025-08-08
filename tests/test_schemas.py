"""
Tests for the Pydantic schemas defined in finai.io.schemas.
"""

from datetime import datetime

import pytest

from finai.io.schemas import (
    Filing,
    Transcript,
    Chunk,
    Event,
    AlignedEvent,
    Label,
    EvalResult,
)


def test_filing_schema():
    """Ensure the Filing model accepts required fields and stores values."""
    f = Filing(
        cik="0000320193",
        ticker="AAPL",
        filing_type="10-K",
        file_time=datetime(2024, 1, 1, 0, 0, 0),
        content="Example filing content",
    )
    assert f.cik == "0000320193"
    assert f.ticker == "AAPL"
    assert f.filing_type == "10-K"


def test_event_schema_defaults():
    """Ensure Event can be instantiated and fields dict stores arbitrary data."""
    now = datetime.utcnow()
    e = Event(
        event_id="evt1",
        ticker="AAPL",
        type="Guidance",
        announce_time=now,
        fields={"metric": "EPS", "new": 1.25, "old": 1.2},
    )
    assert e.fields["metric"] == "EPS"
    assert "new" in e.fields


def test_aligned_event_inherits_event():
    """Ensure AlignedEvent inherits from Event and adds t0 field."""
    now = datetime.utcnow()
    e = AlignedEvent(
        event_id="evt2",
        ticker="AAPL",
        type="Buyback",
        announce_time=now,
        t0=now,
        fields={"amount": 5.0},
    )
    assert isinstance(e, Event)
    assert e.t0 == now


def test_label_schema():
    """Ensure Label model works and stores numeric values."""
    lbl = Label(event_id="evt1", horizon="1d", value=0.0123)
    assert lbl.horizon == "1d"
    assert pytest.approx(lbl.value, rel=1e-9) == 0.0123

