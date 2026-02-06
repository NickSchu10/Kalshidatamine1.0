from datetime import datetime, timezone

from kalshi_bot.models import NormalizedEvent, RawEvent


def test_normalized_event_from_raw_uses_defaults() -> None:
    raw = RawEvent(payload={"type": "trade", "market_id": "ABC"})
    normalized = NormalizedEvent.from_raw(raw)

    assert normalized.event_type == "trade"
    assert normalized.market_id == "ABC"
    assert normalized.sequence is None
    assert isinstance(normalized.timestamp, datetime)


def test_normalized_event_parses_epoch_timestamp() -> None:
    raw = RawEvent(payload={"timestamp": 0})
    normalized = NormalizedEvent.from_raw(raw)

    assert normalized.timestamp == datetime(1970, 1, 1, tzinfo=timezone.utc)
