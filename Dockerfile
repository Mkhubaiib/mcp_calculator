# Multi-stage build for MCP Calculator Server
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy project files
COPY pyproject.toml ./
COPY mcp_server/ ./mcp_server/

# Install the package
RUN pip install --no-cache-dir .


# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app/mcp_server ./mcp_server

# Create non-root user
RUN useradd -m -u 1000 mcpuser && chown -R mcpuser:mcpuser /app
USER mcpuser

# Expose HTTP port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=2.0)" || exit 1

# Run FastMCP server with HTTP transport
CMD ["fastmcp", "run", "mcp_server/server.py:mcp", "--transport", "sse", "--port", "8000", "--host", "0.0.0.0"]
