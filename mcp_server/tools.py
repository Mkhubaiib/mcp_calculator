"""Business logic for calculator tools.

Separating logic keeps protocol handling clean and testable.
"""
from __future__ import annotations
from typing import Any, Dict, Callable
import logging

logger = logging.getLogger("mcp_server.tools")

# Registry of tool metadata and callables
_TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}

class ToolError(Exception):
    """Custom exception for tool-related problems."""

# Decorator to register a tool
def tool(name: str, description: str):
    def wrapper(fn: Callable[[Dict[str, Any]], Any]):
        _TOOL_REGISTRY[name] = {
            "name": name,
            "description": description,
            "callable": fn,
        }
        return fn
    return wrapper

@tool(name="add", description="Add two numbers: a + b")
def tool_add(args: Dict[str, Any]) -> float:
    if "a" not in args or "b" not in args:
        raise ToolError("Missing required arguments: 'a' and 'b' are required")
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
    except (ValueError, TypeError) as e:
        raise ToolError(f"Invalid number format: {str(e)}")
    return a + b

@tool(name="subtract", description="Subtract two numbers: a - b")
def tool_subtract(args: Dict[str, Any]) -> float:
    if "a" not in args or "b" not in args:
        raise ToolError("Missing required arguments: 'a' and 'b' are required")
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
    except (ValueError, TypeError) as e:
        raise ToolError(f"Invalid number format: {str(e)}")
    return a - b

@tool(name="multiply", description="Multiply two numbers: a * b")
def tool_multiply(args: Dict[str, Any]) -> float:
    if "a" not in args or "b" not in args:
        raise ToolError("Missing required arguments: 'a' and 'b' are required")
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
    except (ValueError, TypeError) as e:
        raise ToolError(f"Invalid number format: {str(e)}")
    return a * b

@tool(name="divide", description="Divide two numbers: a / b")
def tool_divide(args: Dict[str, Any]) -> float:
    if "a" not in args or "b" not in args:
        raise ToolError("Missing required arguments: 'a' and 'b' are required")
    try:
        a = float(args.get("a"))
        b = float(args.get("b"))
    except (ValueError, TypeError) as e:
        raise ToolError(f"Invalid number format: {str(e)}")
    if b == 0:
        logger.warning(f"Division by zero attempted with a={a}")
        raise ToolError("Division by zero is not allowed")
    return a / b

def list_tools():
    return [
        {"name": meta["name"], "description": meta["description"]}
        for meta in _TOOL_REGISTRY.values()
    ]

def call_tool(name: str, args: Dict[str, Any]):
    if name not in _TOOL_REGISTRY:
        raise ToolError(f"Unknown tool: {name}")
    fn = _TOOL_REGISTRY[name]["callable"]
    return fn(args)
