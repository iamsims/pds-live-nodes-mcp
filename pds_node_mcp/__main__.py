"""CLI entry point: ``python -m pds_node_mcp [--transport stdio|sse]``."""

from __future__ import annotations

import argparse
import os

from .server import mcp


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PDS node tools MCP server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport type (default: stdio, or MCP_TRANSPORT env var)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "127.0.0.1"),
        help="Host to bind to for SSE (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8001")),
        help="Port for SSE transport (default: 8001)",
    )
    args = parser.parse_args()

    if args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        mcp.run()


if __name__ == "__main__":
    main()
