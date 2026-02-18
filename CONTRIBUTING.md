# Contributing to MCP Calculator

Thank you for your interest in contributing to MCP Calculator! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mcp_calculator.git
   cd mcp_calculator
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. **Create a new branch** for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the code style guidelines below

3. **Write tests** for your changes in the `tests/` directory

4. **Run tests** to ensure everything works:
   ```bash
   pytest tests/ -v
   ```

5. **Commit your changes** with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request** on GitHub

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use type hints for function parameters and return values
- Write docstrings for all public functions and classes
- Keep functions focused and modular
- Use descriptive variable and function names

## Adding New Calculator Tools

When adding new calculator operations:

1. Add the tool definition in `mcp_server/server.py` within the `list_tools()` decorator
2. Implement the tool logic in the `call_tool()` decorator
3. Include proper error handling for edge cases
4. Add comprehensive tests in `tests/test_server.py`
5. Update the README.md with the new tool documentation

Example:
```python
@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        # ... existing tools ...
        Tool(
            name="power",
            description="Calculate base raised to exponent",
            inputSchema={
                "type": "object",
                "properties": {
                    "base": {"type": "number", "description": "The base number"},
                    "exponent": {"type": "number", "description": "The exponent"}
                },
                "required": ["base", "exponent"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
    # ... existing tool handlers ...
    elif name == "power":
        base = arguments.get("base")
        exponent = arguments.get("exponent")
        result = base ** exponent
        return [TextContent(type="text", text=str(result))]
```

## Testing Guidelines

- Write unit tests for all new functionality
- Use `pytest` for testing
- Use `pytest-asyncio` for async tests
- Aim for high test coverage
- Test both success and error cases
- Test edge cases (e.g., division by zero, invalid inputs)

## Reporting Issues

When reporting issues, please include:
- A clear description of the problem
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, package version)
- Error messages or logs

## Questions?

If you have questions about contributing, feel free to:
- Open an issue with the `question` label
- Reach out to the maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints and experiences

Thank you for contributing to MCP Calculator! 🎉
