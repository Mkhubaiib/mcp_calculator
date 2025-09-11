from mcp_server.tools import call_tool

def test_add():
    assert call_tool("add", {"a": 2, "b": 3}) == 5

def test_divide():
    assert call_tool("divide", {"a": 10, "b": 2}) == 5
