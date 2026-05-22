# Investment Committee Supervisor

The **Supervisor** is the central orchestrator of the Crypto Risk Arbitrator system. It acts as the primary interface for users and coordinates tasks between specialist agents.

## Features
- **Multi-Agent Orchestration:** Uses a `SequentialAgent` flow to first consult the Crypto Specialist for data, then the Risk Analyst for assessment.
- **A2A Integration:** Discovers and communicates with specialist agents via the Agent-to-Agent (A2A) protocol.
- **Web Interface:** Provides an interactive Web UI for real-time testing and monitoring.
- **Observability:** Tracks latency and execution flow across the entire agent chain.

## Technical Details

### Orchestration & Communication
The Supervisor serves as the primary system controller:
- **A2A (Agent-to-Agent):** Orchestrates the multi-agent workflow by discovering and delegating tasks to the Crypto Specialist and Risk Analyst via the A2A protocol.
- **Sequential Flow:** Manages the hand-off between specialist agents, ensuring data integrity across the chain.

### Observability & Callbacks
- **End-to-End Latency:** Implements `before_agent_callback` and `after_agent_callback` to track the total performance and latency of the entire multi-agent execution.
- **Service Monitoring:** Monitors A2A connection health and specialist responsiveness.

### Memory Management
- **Hybrid Context:** Supports `VertexAiMemoryBankService` for persistent user interaction history and `InMemoryMemoryService` for ephemeral sessions.
- **Service Selection:** Automatic configuration based on environment variables (`GOOGLE_CLOUD_PROJECT`, `AGENT_ENGINE_ID`).

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
