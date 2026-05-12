"""PDS node tools served over MCP.

Importing this package gives you the configured FastMCP instance:

    from pds_node_mcp import mcp

Five stateless tools, each takes a ``node`` parameter:
``pds_list_missions``, ``pds_list_dataset_dirs``, ``pds_probe_datasets``,
``pds_inspect_collections``, ``pds_resolve_volume``.

To run as a server, use ``python -m pds_node_mcp`` or import ``mcp`` and
call ``mcp.run(...)`` with the transport of your choice.
"""

from __future__ import annotations

from .server import mcp

__all__ = ["mcp"]
