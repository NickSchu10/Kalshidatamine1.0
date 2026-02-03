"""Canonical event models for Kalshi data ingestion."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping


@dataclass(frozen=True)
class RawEvent:
    """Raw event payload as received from the websocket."""

    payload: Mapping[str, Any]
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass(frozen=True)
class NormalizedEvent:
    """Normalized event used internally by downstream consumers."""

    event_type: str
    market_id: str | None
    sequence: int | None
    timestamp: datetime
    payload: Mapping[str, Any]

    @staticmethod
    def from_raw(raw: RawEvent) -> "NormalizedEvent":
        """Create a normalized event from a raw payload.

        This method is intentionally conservative: it maps common fields when present
        but preserves the full payload for future parsing.
        """

        payload = raw.payload
        event_type = str(payload.get("type", "unknown"))
        market_id = payload.get("market_id")
        sequence = payload.get("sequence")
        timestamp_value = payload.get("timestamp")

        if isinstance(timestamp_value, str):
            try:
                timestamp = datetime.fromisoformat(timestamp_value.replace("Z", "+00:00"))
            except ValueError:
                timestamp = raw.received_at
        elif isinstance(timestamp_value, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp_value, tz=timezone.utc)
        else:
            timestamp = raw.received_at

        return NormalizedEvent(
            event_type=event_type,
            market_id=market_id,
            sequence=sequence,
            timestamp=timestamp,
            payload=payload,
        )
