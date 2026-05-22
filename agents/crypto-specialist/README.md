# Crypto Specialist Agent

The **Crypto Specialist** is an autonomous agent built with [Google ADK](https://adk.dev). It specializes in retrieving and interpreting real-time cryptocurrency market data.

## Features
- **Real-time Pricing:** Fetches live prices for any cryptocurrency.
- **Market Context:** Retrieves market cap, 24h volume, and percentage changes.
- **MCP Integration:** Uses a dedicated Model Context Protocol (MCP) server to interface with the CoinGecko API.
- **A2A Protocol:** Exposed as an Agent-to-Agent (A2A) service for discovery and orchestration by the Supervisor.

## Technical Details

### Callbacks & Monitoring
This agent implements specific callbacks for tool execution observability:
- **Tool Interception:** Uses `before_tool_callback` (specifically `on_tool_call`) to intercept and log every call to the CoinGecko bridge, capturing both the tool execution and its computed arguments.
- **Performance:** Employs `before_agent_callback` and `after_agent_callback` for granular latency measurement.

### Communication
- **A2A:** Orchestrated via the Agent-to-Agent protocol for supervisor-level integration.
- **MCP:** Integration with external tools is managed via the Model Context Protocol using `StreamableHTTPConnectionParams` for optimized data streaming.

### Memory
- **Hybrid System:** Supports both `VertexAiMemoryBankService` (persistent) and `InMemoryMemoryService` (local fallback), auto-selected based on environment metadata (`GOOGLE_CLOUD_PROJECT`, `AGENT_ENGINE_ID`).

## Configuration
The agent requires the following environment variables:
- `GOOGLE_API_KEY`: Your Gemini API key.
- `MCP_SERVER_URL`: The URL of the `system-crypto-mcp-server`.

## Local Development
```bash
# Install dependencies
uv sync

# Run the A2A server
GOOGLE_API_KEY="your-key" MCP_SERVER_URL="http://localhost:8000/mcp" uv run python server.py
```

## Deployment
This agent is containerized and ready for Google Cloud Run via the provided `cloudbuild.yaml`.
