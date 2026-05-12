# pds-node-mcp

FastMCP server exposing tools for browsing the NASA Planetary Data System (PDS) discipline-node archives over MCP. The agent calls these tools to walk a node's HTTP directory tree, find PDS3/PDS4 labels, and resolve volume-sets to canonical `DATA_SET_ID`s.

## Supported nodes

| ID | Node | Base URL |
|---|---|---|
| `geo` | Geosciences | https://pds-geosciences.wustl.edu/ |
| `ppi` | Planetary Plasma Interactions | https://pds-ppi.igpp.ucla.edu/ |
| `lroc` | Lunar Reconnaissance Orbiter Camera | https://pds.lroc.im-ldi.com/ |
| `img` | JPL Imaging Node | https://planetarydata.jpl.nasa.gov/ |
| `rms` | Ring-Moon Systems | https://pds-rings.seti.org/ |
| `sbn` | Small Bodies (PSI mirror) | https://sbnarchive.psi.edu/ |
| `atm` | Atmospheres | https://pds-atmospheres.nmsu.edu/ |
| `naif` | NAIF (SPICE kernels) | https://naif.jpl.nasa.gov/ |

Every tool takes a `node` parameter; the server is stateless.

## Tools

Five functional tools, all stateless and all taking a `node` parameter.

| Tool | What it does |
|---|---|
| `pds_list_missions` | Mission directory list for a node. No HTTP — backed by the bundled registry. |
| `pds_list_dataset_dirs` | Lists sub-directories under a path. Cheap HTTP (one listing per call). Each entry tagged `PDS3` / `PDS4` / null from naming convention. |
| `pds_probe_datasets` | Probes specific dataset directories for `voldesc.cat`/`voldesc.sfd` (PDS3) or `bundle*.xml`/`bundle*.lblx` (PDS4). Returns slimmed label fields including `dataset_id`. |
| `pds_inspect_collections` | Walks a PDS4 bundle's subdirs and returns each collection's `logical_identifier` + `title`. |
| `pds_resolve_volume` | For multi-volume holdings (`COISS_2xxx`, `MROM_*`, `cocirs_*`, …) probes children to map each `DATA_SET_ID` to a path. Accepts a fuzzy `dataset_id_hint` for ranking. |

This server contains **no agent-facing prompt content** — no workflow notes, no abbreviation tables, no per-node planning instructions. Callers are expected to bring their own system prompt with that context. Keeping the boundary clean lets you redeploy without re-shipping prompts.

## Run locally

```sh
uv venv && source .venv/bin/activate
uv pip install -e .

# stdio (default — used by MCP clients that spawn the server as a subprocess)
python -m pds_node_mcp

# SSE on :8001
python -m pds_node_mcp --transport sse --port 8001
```

Use the `pds-node-mcp` console script after install for the same behavior.

## Deploy to FastMCP Cloud

The repository is FastMCP-cloud-ready — `fastmcp` is a declared dependency and the package exposes `pds_node_mcp.mcp` as the FastMCP instance. Point a new FastMCP Cloud project at this repo and set the entry to `pds_node_mcp` (or `pds_node_mcp.server:mcp`).

## Connect from a client

```python
# pydantic-ai
from pydantic_ai.mcp import MCPServerStdio, MCPServerStreamableHTTP

# Spawn locally over stdio
stdio = MCPServerStdio("python", args=["-m", "pds_node_mcp"])

# Or connect to the deployed instance
hosted = MCPServerStreamableHTTP(
    url="https://<your-app>.fastmcp.app/mcp",
    headers={"Authorization": f"Bearer {token}"},
)
```

## Origin

Extracted from `pydantic_code/tools/` so the server can be deployed independently of the agent codebase that consumes it.
