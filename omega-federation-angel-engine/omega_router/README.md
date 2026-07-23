# Omega Router Skeleton

Safe local-first continuity routing skeleton.

## Principles

- Never depend on the UI.
- Local storage is the continuity spine.
- Provider models are callable nodes.
- No arbitrary shell execution from model output.
- Preserve source artifacts.

## Files

- `router.py` — routing runtime.
- `permission_gate.py` — Repo 120 gate.
- `bus_writer.py` — JSONL/state helpers.
- `route_registry.json` — route definitions.

## Runtime Output

Generated automatically:

- `runtime/comm_bus.jsonl`
- `runtime/router_events.jsonl`
- `runtime/terminal_router_state.json`

## Run

```bash
cd omega_router
python router.py
```

## Example Payload

```text
@route:reason
Summarize the current checkpoint.
```

## Next Build Targets

- clipboard watcher daemon
- Termux notification integration
- SQLite continuity index
- local GGUF/Ollama connector
- Gemini API transport layer
- Drive/Mem checkpoint adapters
- RouterOS ingress relay
