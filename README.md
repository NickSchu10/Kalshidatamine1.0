# Kalshi Strategy Engine (Scaffold)

This repository contains the initial scaffold for a Kalshi market data ingestion and
strategy execution engine. The goal is to build the system in batches so each layer
is testable before integration.

## Batch 1: Data ingestion & normalization (current)

- Establish a canonical event schema.
- Provide append-only storage for raw events.
- Provide a normalizer that produces a deterministic internal event format.
- Provide a lightweight async event bus for downstream consumers.

## Next batches (planned)

1. Strategy execution framework (parallel strategy runner).
2. Inefficiency detection & signal scoring.
3. Risk management & sizing layer.
4. Execution layer with paper/live adapters.
5. Observability and operational tooling.

## Layout

```
kalshi_bot/
  models.py            # Canonical event models
  storage.py           # Append-only JSONL storage
  stream.py            # Normalization and event bus
  websocket_client.py  # Websocket client interface + fakes
```

## Quick start (dev)

This codebase is intentionally dependency-light. The websocket implementation
is stubbed so the ingestion layer can be tested in isolation.

```
python -m kalshi_bot.websocket_client
```

## Notes

- The websocket protocol specifics are intentionally abstracted behind
  `WebsocketClient`. You can add a real Kalshi implementation once credentials
  and endpoints are finalized.
- For data durability, JSONL is used as a simple append-only format.

