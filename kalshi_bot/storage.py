"""Append-only storage for raw events."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from .models import RawEvent


class JsonlEventStore:
    """Persist raw events in an append-only JSONL file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, event: RawEvent) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event), default=str) + "\n")

    def append_many(self, events: Iterable[RawEvent]) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            for event in events:
                handle.write(json.dumps(asdict(event), default=str) + "\n")
