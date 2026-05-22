# Investment Committee Supervisor

The **Supervisor** is the central orchestrator of the Crypto Risk Arbitrator system. It acts as the primary interface for users and coordinates tasks between specialist agents.

## Features
- **Multi-Agent Orchestration:** Uses a `SequentialAgent` flow to first consult the Crypto Specialist for data, then the Risk Analyst for assessment.
- **A2A Integration:** Discovers and communicates with specialist agents via the Agent-to-Agent (A2A) protocol.
- **Web Interface:** Provides an interactive Web UI for real-time testing and monitoring.
- **Observability:** Tracks latency and execution flow across the entire agent chain.

## Configuration
The supervisor requires the following environment variables:
- `GOOGLE_API_KEY`: Your Gemini API key.
- `CRYPTO_AGENT_URL`: The URL of the Crypto Specialist A2A server.
- `RISK_AGENT_URL`: The URL of the Risk Analyst A2A server.

## Local Development
```bash
# Install dependencies
uv sync

# Run the Supervisor Web UI
GOOGLE_API_KEY="your-key" CRYPTO_AGENT_URL="http://localhost:8001" RISK_AGENT_URL="http://localhost:8002" uv run adk web supervisor
```

## Deployment
Deployed to Google Cloud Run, serving as the system's public entry point.
