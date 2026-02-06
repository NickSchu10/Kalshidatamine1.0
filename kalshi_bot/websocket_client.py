"""Websocket client interface and testing doubles."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any, Mapping

from .models import RawEvent


class WebsocketClient:
    """Interface for streaming raw websocket events."""

    async def connect(self) -> None:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    async def listen(self) -> AsyncIterator[RawEvent]:
        raise NotImplementedError


@dataclass
class FakeWebsocketClient(WebsocketClient):
    """Fake websocket client for local testing."""

    events: list[Mapping[str, Any]]
    delay_s: float = 0.0

    async def connect(self) -> None:
        return None

    async def disconnect(self) -> None:
        return None

    async def listen(self) -> AsyncIterator[RawEvent]:
        for event in self.events:
            if self.delay_s:
                await asyncio.sleep(self.delay_s)
            yield RawEvent(payload=event)


async def demo() -> None:
    client = FakeWebsocketClient(
        events=[
            {"type": "trade", "market_id": "EXAMPLE", "sequence": 1},
            {"type": "orderbook", "market_id": "EXAMPLE", "sequence": 2},
        ],
        delay_s=0.1,
    )

    await client.connect()
    async for event in client.listen():
        print(event)
    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(demo())
