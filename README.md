# MCP Calculator Server

A Model Context Protocol (MCP) server that provides calculator operations via **FastMCP**.

## Features

- ✅ **FastMCP Framework** - Built with FastMCP for simplified MCP server development
- ✅ **SSE Transport** - Server-Sent Events transport for MCP clients
- ✅ **Container Ready** - Docker and docker-compose support for easy deployment
- ✅ **4 Calculator Tools** - add, subtract, multiply, divide
- ✅ **Type Safety** - Automatic input validation with type hints
- ✅ **Error Handling** - Graceful handling of edge cases (division by zero, invalid inputs)

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

```bash
# Development mode with auto-reload
fastmcp run mcp_server/server.py:mcp --transport sse --port 8000 --reload

# Production mode
fastmcp run mcp_server/server.py:mcp --transport sse --port 8000
```

### Testing with MCP Inspector

```bash
# Interactive development mode with web UI
fastmcp dev inspector mcp_server/server.py:mcp
```

This opens a web interface to test your tools interactively.

### Using Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build and run manually
docker build -t mcp-calculator .
docker run -p 8000:8000 mcp-calculator
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `add` | Add two numbers | `a` (number), `b` (number) |
| `subtract` | Subtract b from a | `a` (number), `b` (number) |
| `multiply` | Multiply two numbers | `a` (number), `b` (number) |
| `divide` | Divide a by b | `a` (number), `b` (number, cannot be zero) |

### Project Structure

```
mcp_calculator/
├── mcp_server/
│   ├── __init__.py
│   └── server.py          # FastMCP server implementation
├── Dockerfile             # Container image definition
├── docker-compose.yml     # Multi-container orchestration
├── pyproject.toml
└── README.md
```

## Requirements

- Python >= 3.10
- FastMCP (`fastmcp>=3.0.0`)
- Uvicorn for HTTP server (`uvicorn[standard]>=0.35.0`)

## Docker Deployment

The server is designed for containerized deployment:

1. **Build**: `docker build -t mcp-calculator .`
2. **Run**: `docker run -p 8000:8000 mcp-calculator`
3. **Access**: `http://localhost:8000`

## References

- [Model Context Protocol](https://modelcontextprotocol.io/)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
