"""Tests for MCP Calculator Server."""
import pytest
from mcp_server.server import call_tool


@pytest.mark.asyncio
async def test_add():
    """Test addition operation."""
    result = await call_tool("add", {"a": 5, "b": 3})
    assert len(result) == 1
    assert result[0].text == "8.0"


@pytest.mark.asyncio
async def test_subtract():
    """Test subtraction operation."""
    result = await call_tool("subtract", {"a": 10, "b": 4})
    assert len(result) == 1
    assert result[0].text == "6.0"


@pytest.mark.asyncio
async def test_multiply():
    """Test multiplication operation."""
    result = await call_tool("multiply", {"a": 6, "b": 7})
    assert len(result) == 1
    assert result[0].text == "42.0"


@pytest.mark.asyncio
async def test_divide():
    """Test division operation."""
    result = await call_tool("divide", {"a": 20, "b": 4})
    assert len(result) == 1
    assert result[0].text == "5.0"


@pytest.mark.asyncio
async def test_divide_by_zero():
    """Test division by zero error handling."""
    result = await call_tool("divide", {"a": 10, "b": 0})
    assert len(result) == 1
    assert "Division by zero" in result[0].text


@pytest.mark.asyncio
async def test_invalid_tool():
    """Test calling an unknown tool."""
    result = await call_tool("unknown", {"a": 1, "b": 2})
    assert len(result) == 1
    assert "Unknown tool" in result[0].text


@pytest.mark.asyncio
async def test_missing_argument():
    """Test missing required argument."""
    result = await call_tool("add", {"a": 5})
    assert len(result) == 1
    assert "Missing required argument" in result[0].text


@pytest.mark.asyncio
async def test_invalid_argument_type():
    """Test invalid argument type."""
    result = await call_tool("add", {"a": "not_a_number", "b": 5})
    assert len(result) == 1
    assert "Invalid argument type" in result[0].text
