"""MCP Calculator Server using FastMCP.

This server provides basic calculator operations (add, subtract, multiply, divide)
via the Model Context Protocol. It uses SSE transport for container deployment.
"""
import logging
from fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("mcp-calculator")

# Create FastMCP server instance
mcp = FastMCP(
    name="Calculator Server",
    version="0.2.0",
)


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    result = a + b
    logger.info(f"add({a}, {b}) = {result}")
    return result


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract second number from first number.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Difference of a minus b
    """
    result = a - b
    logger.info(f"subtract({a}, {b}) = {result}")
    return result


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Product of a and b
    """
    result = a * b
    logger.info(f"multiply({a}, {b}) = {result}")
    return result


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide first number by second number.
    
    Args:
        a: Numerator
        b: Denominator (cannot be zero)
    
    Returns:
        Quotient of a divided by b
    
    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    
    result = a / b
    logger.info(f"divide({a}, {b}) = {result}")
    return result
