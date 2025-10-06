from mcp_server.tools import call_tool, ToolError
import pytest

def test_add():
    assert call_tool("add", {"a": 2, "b": 3}) == 5

def test_divide():
    assert call_tool("divide", {"a": 10, "b": 2}) == 5

# Edge case tests
def test_divide_by_zero():
    """Test that division by zero raises appropriate error."""
    with pytest.raises(ToolError, match="Division by zero is not allowed"):
        call_tool("divide", {"a": 10, "b": 0})

def test_missing_arguments():
    """Test that missing arguments raise appropriate error."""
    with pytest.raises(ToolError, match="Missing required arguments"):
        call_tool("add", {"a": 5})
    
    with pytest.raises(ToolError, match="Missing required arguments"):
        call_tool("subtract", {"b": 3})
    
    with pytest.raises(ToolError, match="Missing required arguments"):
        call_tool("multiply", {})

def test_invalid_number_format():
    """Test that invalid number formats raise appropriate error."""
    with pytest.raises(ToolError, match="Invalid number format"):
        call_tool("add", {"a": "not a number", "b": 5})
    
    with pytest.raises(ToolError, match="Invalid number format"):
        call_tool("multiply", {"a": 10, "b": "invalid"})

def test_unknown_tool():
    """Test that unknown tool names raise appropriate error."""
    with pytest.raises(ToolError, match="Unknown tool"):
        call_tool("unknown_operation", {"a": 1, "b": 2})

def test_subtract():
    """Test subtraction operation."""
    assert call_tool("subtract", {"a": 10, "b": 3}) == 7
    assert call_tool("subtract", {"a": 5, "b": 10}) == -5

def test_multiply():
    """Test multiplication operation."""
    assert call_tool("multiply", {"a": 4, "b": 5}) == 20
    assert call_tool("multiply", {"a": -2, "b": 3}) == -6

def test_float_operations():
    """Test operations with floating point numbers."""
    assert call_tool("add", {"a": 1.5, "b": 2.3}) == pytest.approx(3.8)
    assert call_tool("divide", {"a": 7.5, "b": 2.5}) == pytest.approx(3.0)
    assert call_tool("multiply", {"a": 2.5, "b": 4.0}) == pytest.approx(10.0)

