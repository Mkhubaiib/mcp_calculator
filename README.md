# MCP Calculator Server

A Model Context Protocol (MCP) server that provides calculator operations for MCP clients.

## Features

- ✅ **Official MCP SDK** - Built with the official `mcp` Python package
- ✅ **stdio Transport** - Standard MCP communication protocol
- ✅ **4 Calculator Tools** - add, subtract, multiply, divide
- ✅ **Type Safety** - Full input validation with JSON schemas
- ✅ **Error Handling** - Graceful handling of edge cases (division by zero, invalid inputs)
- ✅ **Well Tested** - Comprehensive test coverage with pytest

## Installation

```bash
# Clone the repository
git clone https://github.com/Mkhubaiib/mcp_calculator.git
cd mcp_calculator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Usage

### Running the Server

Run the MCP server using either method:

```bash
# Using the entry point command
mcp-calculator

# Or using Python module syntax
python -m mcp_server.server
```

The server communicates via stdio (stdin/stdout) using the MCP protocol.

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `add` | Add two numbers | `a` (number), `b` (number) |
| `subtract` | Subtract b from a | `a` (number), `b` (number) |
| `multiply` | Multiply two numbers | `a` (number), `b` (number) |
| `divide` | Divide a by b | `a` (number), `b` (number, cannot be zero) |

## Development

### Running Tests

```bash
pip install -e ".[dev]"
pytest
```

### Project Structure

```
mcp_calculator/
├── mcp_server/
│   ├── __init__.py
│   └── server.py          # Main MCP server
├── tests/
│   └── test_server.py     # Unit tests
├── pyproject.toml
└── README.md
```

## Troubleshooting

- Verify absolute path in `claude_desktop_config.json`
- Ensure Python >= 3.10
- Check Claude Desktop logs (Help → View Logs)

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
Requirements

- Python >= 3.10
- Official MCP SDK (`mcp>=1.0.0`