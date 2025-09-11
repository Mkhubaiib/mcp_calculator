"""Protocol models for a minimal MCP-like interaction layer.

This is a *simplified* educational subset, not the full official spec.
Each inbound JSON message is validated against one of these Pydantic models.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Literal, Dict, Any
import uuid

# ----- Base Message -----
class BaseMessage(BaseModel):
    type: str = Field(..., description="Message discriminator")

# ----- Client -> Server messages -----
class InitializeMessage(BaseMessage):
    type: Literal["initialize"]
    client: str
    version: str

class PingMessage(BaseMessage):
    type: Literal["ping"]
    nonce: Optional[str] = None

class ListToolsMessage(BaseMessage):
    type: Literal["list_tools"]

class CallToolMessage(BaseMessage):
    type: Literal["call_tool"]
    name: str
    args: Dict[str, Any] = {}

# Union style factory (manual to keep it simple for a beginner)
MESSAGE_TYPE_MAP = {
    "initialize": InitializeMessage,
    "ping": PingMessage,
    "list_tools": ListToolsMessage,
    "call_tool": CallToolMessage,
}

def parse_message(data: Dict[str, Any]) -> BaseMessage:
    """Parse raw dict into a concrete message model.

    Raises ValueError if the message is unknown or validation fails.
    """
    t = data.get("type")
    model_cls = MESSAGE_TYPE_MAP.get(t)
    if not model_cls:
        raise ValueError(f"Unknown message type: {t}")
    return model_cls(**data)

# ----- Server -> Client messages -----
class InitializedMessage(BaseMessage):
    type: Literal["initialized"]
    session_id: str
    server: str = "mcp-calculator"
    capabilities: Dict[str, Any] = Field(default_factory=lambda: {"tools": True})

    @classmethod
    def create(cls) -> "InitializedMessage":
        return cls(type="initialized", session_id=str(uuid.uuid4()))

class PongMessage(BaseMessage):
    type: Literal["pong"]
    nonce: Optional[str] = None

class ToolsListMessage(BaseModel):
    type: Literal["tools_list"] = "tools_list"
    tools: list

class ToolResultMessage(BaseModel):
    type: Literal["tool_result"] = "tool_result"
    name: str
    result: Any

class ErrorMessage(BaseModel):
    type: Literal["error"] = "error"
    error: str
    details: Optional[Dict[str, Any]] = None

__all__ = [
    "BaseMessage",
    "InitializeMessage",
    "PingMessage",
    "ListToolsMessage",
    "CallToolMessage",
    "InitializedMessage",
    "PongMessage",
    "ToolsListMessage",
    "ToolResultMessage",
    "ErrorMessage",
    "parse_message",
]
