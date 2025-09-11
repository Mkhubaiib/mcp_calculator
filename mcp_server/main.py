"""FastAPI application exposing a WebSocket implementing a minimal MCP-like protocol.

Flow:
1. Client connects to ws://host/mcp
2. Must send an `initialize` message first.
3. Then may send: ping, list_tools, call_tool.

All messages and responses are JSON. Errors return a unified shape.
"""
from __future__ import annotations
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json
import logging

from .protocol import (
    parse_message,
    InitializeMessage,
    PingMessage,
    ListToolsMessage,
    CallToolMessage,
    InitializedMessage,
    PongMessage,
    ToolsListMessage,
    ToolResultMessage,
    ErrorMessage,
)
from .tools import list_tools, call_tool, ToolError
from .logging_config import configure_logging

logger = logging.getLogger("mcp_server")
configure_logging()

app = FastAPI(title="MCP Calculator Server")

@app.get("/")
async def root():
    return {"message": "MCP Calculator Server. Connect via WebSocket at /mcp"}

@app.get("/demo")
async def demo_page():
    """Serve a tiny HTML demo page for manual testing."""
    return HTMLResponse(
        """
        <html><body>
        <h3>WebSocket Demo</h3>
        <pre id='log'></pre>
        <script>
        const log = (m)=>document.getElementById('log').textContent += m + "\n";
        const ws = new WebSocket("ws://" + location.host + "/mcp");
        ws.onopen = ()=>{
            log("OPEN");
            ws.send(JSON.stringify({type:'initialize', client:'browser', version:'1.0'}));
        };
        ws.onmessage = (ev)=>log("RECV: " + ev.data);
        ws.onerror = (e)=>log("ERR: " + e);
        ws.onclose = ()=>log("CLOSE");
        setTimeout(()=>ws.send(JSON.stringify({type:'list_tools'})), 500);
        setTimeout(()=>ws.send(JSON.stringify({type:'call_tool', name:'add', args:{a:2,b:3}})), 1000);
        </script>
        </body></html>
        """
    )

def _serialize(model):
    """Helper to convert Pydantic model or plain dict into JSON-serializable dict."""
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model

def _handle_parsed_message(msg, state):
    """Return a server message model (or ErrorMessage) for a parsed client message.

    state is a dict so we can mutate (e.g. mark initialized) without globals.
    """
    if isinstance(msg, InitializeMessage):
        state["initialized"] = True
        return InitializedMessage.create()
    if not state.get("initialized"):
        return ErrorMessage(error="Must initialize first")
    if isinstance(msg, PingMessage):
        return PongMessage(type="pong", nonce=msg.nonce)
    if isinstance(msg, ListToolsMessage):
        return ToolsListMessage(tools=list_tools())
    if isinstance(msg, CallToolMessage):
        try:
            result = call_tool(msg.name, msg.args)
            return ToolResultMessage(name=msg.name, result=result)
        except ToolError as te:
            return ErrorMessage(error=str(te))
        except Exception:
            logger.exception("Unhandled tool error")
            return ErrorMessage(error="Internal error")
    return ErrorMessage(error="Unsupported message")

@app.websocket("/mcp")
async def mcp_socket(ws: WebSocket):
    await ws.accept()
    state = {"initialized": False}

    async def send_obj(obj):
        await ws.send_text(json.dumps(_serialize(obj)))

    try:
        while True:
            raw = await ws.receive_text()
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await send_obj(ErrorMessage(error="Invalid JSON"))
                continue
            try:
                msg = parse_message(data)
            except Exception as e:
                await send_obj(ErrorMessage(error=str(e)))
                continue
            reply = _handle_parsed_message(msg, state)
            await send_obj(reply)
    except WebSocketDisconnect:
        logger.info("Client disconnected")
    except Exception:
        logger.exception("Fatal WebSocket handler error")
        try:
            await send_obj(ErrorMessage(error="Server crash"))
        except Exception:
            pass
