from mcp.server.fastmcp import FastMCP

# FastMCP makes it trivial to build your own MCP server in Python
server = FastMCP("Math Tools Server")


@server.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@server.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@server.tool()
def power(base: float, exponent: float) -> float:
    """Raise base to the power of exponent."""
    return base**exponent


@server.tool()
def summarize_numbers(numbers: list[float]) -> dict:
    """Return the sum, average, min and max of a list of numbers."""
    return {
        "sum": sum(numbers),
        "average": sum(numbers) / len(numbers),
        "min": min(numbers),
        "max": max(numbers),
    }


if __name__ == "__main__":
    # Run the MCP server over stdio transport — Pydantic AI will launch this
    # as a subprocess and communicate with it via stdin/stdout
    server.run(transport="stdio")
