#!/usr/bin/env bash
set -euo pipefail
uvicorn mcp_server.main:app --reload --port 8000
