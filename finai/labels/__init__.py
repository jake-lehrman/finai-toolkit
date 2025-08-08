"""
Label generation utilities for supervised learning tasks.

This module provides functions to compute target variables for models,
such as returns over various horizons, abnormal returns, volatility spikes,
and classification labels for price movements. All labels are computed
relative to an event's alignment timestamp to avoid lookahead bias.
"""

__all__ = []
