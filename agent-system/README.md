# Agent System — Crypto Price Agent

An ADK-based agent that retrieves real-time cryptocurrency prices
via a remote MCP server deployed on Cloud Run.

## Quick start

```bash
cd agent-system
uv sync                       # install dependencies
uv run adk web                # launch the playground UI
```

## Architecture

```
agent-system/
├── app/
│   ├── __init__.py
│   └── agent.py              # Agent definition + MCP toolset
├── pyproject.toml
└── README.md
```

The agent connects to the remote MCP server at:
`https://system-crypto-mcp-server-823002731253.us-central1.run.app/mcp`

using the **Streamable HTTP** transport (`StreamableHTTPConnectionParams`).
