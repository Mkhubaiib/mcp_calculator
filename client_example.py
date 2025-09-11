"""Minimal example WebSocket client for the MCP calculator server.

Run after starting the server:
    python client_example.py
"""
import asyncio
import json
import websockets

URL = "ws://localhost:8000/mcp"

async def run():
    async with websockets.connect(URL) as ws:
        # 1. Initialize session
        await ws.send(json.dumps({"type": "initialize", "client": "py-client", "version": "1.0"}))
        print("-> initialize sent")
        print("<-", await ws.recv())

        # 2. List tools
        await ws.send(json.dumps({"type": "list_tools"}))
        print("-> list_tools sent")
        print("<-", await ws.recv())

        # 3. Call add tool
        await ws.send(json.dumps({"type": "call_tool", "name": "add", "args": {"a": 5, "b": 7}}))
        print("-> call_tool add sent")
        print("<-", await ws.recv())

        # 4. Ping
        await ws.send(json.dumps({"type": "ping", "nonce": "123"}))
        print("-> ping sent")
        print("<-", await ws.recv())

if __name__ == "__main__":
    asyncio.run(run())
