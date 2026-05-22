# Crypto Specialist Agent

The **Crypto Specialist** is an autonomous agent built with [Google ADK](https://adk.dev). It specializes in retrieving and interpreting real-time cryptocurrency market data.

## Features
- **Real-time Pricing:** Fetches live prices for any cryptocurrency.
- **Market Context:** Retrieves market cap, 24h volume, and percentage changes.
- **MCP Integration:** Uses a dedicated Model Context Protocol (MCP) server to interface with the CoinGecko API.
- **A2A Protocol:** Exposed as an Agent-to-Agent (A2A) service for discovery and orchestration by the Supervisor.

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
