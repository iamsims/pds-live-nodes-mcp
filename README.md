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

## Response size limits

Every tool that can return a variable-size or unbounded list takes a bounding parameter. None of them accept `None`/unset to mean "no limit" — each has a real default and a hard max, so an agent can't cause an oversized response either by omitting the param or by passing something huge.

| Tool | Param | Shape | Default | Max | Why this number |
|---|---|---|---|---|---|
| `pds_list_dataset_dirs` | `limit` | output cap (rows returned) | 500 | 500 | Each row is 3 short strings (`name`, `path`, `pds_hint`) — cheap. 500 comfortably covers the largest known flat listing (PPI, ~767 dataset dirs pre-filter) while still bounding the response. `total`/`filtered_total` always report the pre-limit count, so a truncated response is detectable. |
| `pds_probe_datasets` | `limit` | output cap (rows returned, **per path**) | 20 | 20 | Each row carries a nested `fields` dict (slimmed label content) — meaningfully heavier than a directory-listing row. Realistic hybrid dirs (both PDS3 and PDS4 labels) produce at most 2-3 results per path, so 20 is a safety ceiling, not a value normal calls approach. |
| `pds_probe_datasets` | `paths` | input cap (list truncated on the way in) | — | 20 | Bounds *fan-out*, not row count: each path triggers its own directory fetch + recursion, so an unbounded `paths` list is a request-count problem, not a payload-size problem. Silently truncated to the first 20 rather than exposed as a tunable param, since batching more than ~20 probes in one call isn't a real workflow. |
| `pds_inspect_collections` | `max_subdirs` | work cap (subdirs walked, not rows returned) | 20 | 50 | Bounds *how much the tool does*, not how much it returns — each subdir walked is a separate label fetch. 50 is looser than the two output caps above because collections are typically few per bundle; the cap exists to stop pathological bundles with hundreds of subdirs from triggering that many fetches in one call. |
| `pds_resolve_volume` | `sample` | work cap (children probed, not rows returned) | 8 | 20 | Same shape as `max_subdirs` — bounds probe fan-out on a volume-set's children, ordered to try the most likely matches (via `dataset_id_hint`) first. Default is lower (8, not 20) because this tool is normally used to disambiguate one `DATA_SET_ID` among siblings, not to enumerate all of them; the max still allows an agent to widen the search on a large volume-set. |
| `pds_list_missions` | — | — | — | — | No limit param. Backed by a hardcoded in-memory registry, no HTTP call, no unbounded external input — list size is fixed by what's in the registry. |

Two different clamp shapes show up above:
- **Output caps** (`pds_list_dataset_dirs.limit`, `pds_probe_datasets.limit`) bound the size of the *response payload* — sized by how expensive one result row is to represent (a few strings vs. a nested label dict).
- **Work/fan-out caps** (`pds_probe_datasets.paths`, `pds_inspect_collections.max_subdirs`, `pds_resolve_volume.sample`) bound the number of *upstream HTTP calls* a single tool invocation triggers — sized by how many requests are reasonable to issue serially before a call becomes slow or hammers the upstream PDS node.

All are implemented the same way: `param = min(param, MAX)`, applied unconditionally right after the function signature, before any work happens. `max_subdirs` and `sample` additionally floor at 1 (`max(1, min(param, MAX))`) since a 0 or negative value would otherwise skip the walk/probe entirely; the two `limit` params skip that floor because a non-positive limit just yields an empty (harmless) result list.

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
