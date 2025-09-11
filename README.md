# MCP Calculator Server (Python)

A beginner-friendly Model Context Protocol (MCP) server that exposes a simple calculator tool (add, subtract, multiply, divide) over WebSocket using FastAPI.

## What is MCP?
Model Context Protocol (MCP) is a structured, message-based protocol that lets AI models/tools/clients exchange capabilities and context safely. A server implements tools/resources and communicates over JSON messages (often via WebSocket or stdio). A client connects, performs a handshake (`initialize`), then invokes tools (`call_tool`).

## Features
- FastAPI + WebSocket endpoint `/mcp`.
- Basic MCP message types: `initialize`, `ping`, `list_tools`, `call_tool`.
- Simple calculator operations with validation.
- Structured error responses.
- Basic logging middleware.

## Project Structure
```
 mcp_calculator/
 ├── README.md                # Project overview & instructions
 ├── pyproject.toml           # Dependencies & packaging metadata
 ├── mcp_server/              # Source package
 │   ├── __init__.py
 │   ├── main.py              # FastAPI app + WebSocket handler
 │   ├── protocol.py          # Pydantic models for MCP messages
 │   ├── tools.py             # Calculator tool implementations
 │   └── logging_config.py    # Logging setup
 ├── tests/
 │   └── test_tools.py        # Basic unit tests for calculator logic
 ├── scripts/
 │   └── run_dev.sh           # Helper script to run server
 └── client_example.py        # Minimal WebSocket client example
```

## Install & Run
```bash
# (Optional) create virtual env
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e .

# Run server (reload for dev)
uvicorn mcp_server.main:app --reload --port 8000
```

WebSocket URL: `ws://localhost:8000/mcp`

## Test
```bash
pytest -q
```

## Try Client Example
In another terminal after server is running:
```bash
python client_example.py
```

## Example MCP Flow (JSON)
1. Client connects and sends `initialize`:
```json
{"type":"initialize","client":"demo","version":"1.0"}
```
2. Server replies with capabilities + session id.
3. Client lists tools:
```json
{"type":"list_tools"}
```
4. Client calls add:
```json
{"type":"call_tool","name":"add","args":{"a":5,"b":7}}
```
5. Server responds:
```json
{"type":"tool_result","name":"add","result":12}
```

## Best Practices (Summary)
- Validate all inbound messages with schemas (Pydantic models here).
- Keep protocol layer separate from business logic (`tools.py`).
- Return structured errors with a consistent shape.
- Use logging levels: INFO for flow, DEBUG for payloads (avoid secrets), WARNING/ERROR for issues.
- Add timeouts & rate limiting (future enhancement) for production.
- Consider versioning and compatibility in `initialize` handshake.
- Write unit tests for pure logic (calculator) and integration tests for protocol.

