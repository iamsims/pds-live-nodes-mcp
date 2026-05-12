"""PDS node tools served over MCP.

Importing this package gives you the configured FastMCP instance:

    from pds_node_mcp import mcp

To run as a server, use ``python -m pds_node_mcp`` or import ``mcp`` and
call ``mcp.run(...)`` with the transport of your choice.
"""

from __future__ import annotations

from .server import mcp

__all__ = ["mcp"]
