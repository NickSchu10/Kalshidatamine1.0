"""Normalization and event bus utilities."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from typing import Any, Mapping

from .models import NormalizedEvent, RawEvent


class Normalizer:
    """Convert raw websocket payloads into normalized events."""

    def normalize(self, payload: Mapping[str, Any]) -> NormalizedEvent:
        return NormalizedEvent.from_raw(RawEvent(payload=payload))


class EventBus:
    """Simple async event bus to fan out normalized events."""

    def __init__(self, max_queue_size: int = 0) -> None:
        self._queues: list[asyncio.Queue[NormalizedEvent]] = []
        self._max_queue_size = max_queue_size

    def subscribe(self) -> asyncio.Queue[NormalizedEvent]:
        queue: asyncio.Queue[NormalizedEvent] = asyncio.Queue(maxsize=self._max_queue_size)
        self._queues.append(queue)
        return queue

    async def publish(self, event: NormalizedEvent) -> None:
        for queue in self._queues:
            await queue.put(event)

    async def stream(self) -> AsyncIterator[NormalizedEvent]:
        queue = self.subscribe()
        while True:
            yield await queue.get()
