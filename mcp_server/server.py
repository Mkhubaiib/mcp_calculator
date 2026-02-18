"""MCP Calculator Server using official SDK.

This server provides basic calculator operations (add, subtract, multiply, divide)
via the Model Context Protocol. It uses stdio transport for Claude Desktop compatibility.
"""
import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp-calculator")

# Create MCP server instance
app = Server("mcp-calculator")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available calculator tools."""
    return [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="subtract",
            description="Subtract second number from first number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "First number"},
                    "b": {"type": "number", "description": "Second number"},
                },
                "required": ["a", "b"],
            },
        ),
        Tool(
            name="divide",
            description="Divide first number by second number",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {"type": "number", "description": "Numerator"},
                    "b": {"type": "number", "description": "Denominator (cannot be zero)"},
                },
                "required": ["a", "b"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute calculator operations."""
    try:
        a = float(arguments["a"])
        b = float(arguments["b"])
        
        if name == "add":
            result = a + b
        elif name == "subtract":
            result = a - b
        elif name == "multiply":
            result = a * b
        elif name == "divide":
            if b == 0:
                return [TextContent(type="text", text="Error: Division by zero is not allowed")]
            result = a / b
        else:
            return [TextContent(type="text", text=f"Error: Unknown tool {name}")]
        
        logger.info(f"Executed {name}({a}, {b}) = {result}")
        return [TextContent(type="text", text=str(result))]
    
    except KeyError as e:
        return [TextContent(type="text", text=f"Error: Missing required argument {e}")]
    except (ValueError, TypeError) as e:
        return [TextContent(type="text", text=f"Error: Invalid argument type - {e}")]
    except Exception as e:
        logger.exception("Unexpected error in tool execution")
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server using stdio transport."""
    logger.info("Starting MCP Calculator Server")
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


def run():
    """Entry point for the server."""
    asyncio.run(main())


if __name__ == "__main__":
    run()
