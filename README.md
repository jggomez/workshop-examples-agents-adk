# Crypto Risk Arbitrator — Multi-Agent System

A professional multi-agent investment analysis platform built with [Google ADK](https://adk.dev), using the **Agent-to-Agent (A2A)** protocol and **Model Context Protocol (MCP)**.

## Architecture

```mermaid
graph TB
    subgraph Client_Layer [User Interface]
        User((User))
    end

    subgraph Orchestration_Layer [Orchestration]
        Supervisor[Supervisor Agent]
    end

    subgraph Specialist_Layer [Specialized Agents]
        Crypto[Crypto Specialist]
        Risk[Risk Analyst]
    end

    subgraph Data_Layer [Data & Tools]
        MCPServer[MCP Server]
        CoinGecko[(CoinGecko API)]
    end

    subgraph Platform_Layer [Shared Services]
        MemoryBank[(Vertex AI Memory Bank / In-Memory)]
        Observability[[Lifecycle Callbacks & Logging]]
    end

    User -->|Web UI / API| Supervisor
    Supervisor -->|A2A Protocol| Crypto
    Supervisor -->|A2A Protocol| Risk
    Crypto -->|MCP / Streamable HTTP| MCPServer
    MCPServer -->|HTTPS| CoinGecko

    %% Shared Platform Connections
    Supervisor -.-> MemoryBank
    Crypto -.-> MemoryBank
    Risk -.-> MemoryBank

    Supervisor -.-> Observability
    Crypto -.-> Observability
    Risk -.-> Observability
```

## Quick Start

### Local Execution (Full Stack)
The easiest way to run the entire system locally is using the provided automation script:

```bash
# Set your API Key
export GOOGLE_API_KEY="your-gemini-api-key"

# Run all services (MCP, Specialists, and Supervisor Web UI)
./run_local.sh
```
The **Supervisor Web UI** will be available at [http://localhost:8005](http://localhost:8005).

### Automated Cloud Deployment
To deploy the entire system to Google Cloud Run:

```bash
export GOOGLE_API_KEY="your-gemini-api-key"
./deploy.sh
```

## Project Structure

| Component | Path | Purpose |
| :--- | :--- | :--- |
| **Root** | `.` | Global configuration and orchestration scripts. |
| **Supervisor** | `agents/supervisor` | System orchestrator and Web UI. |
| **Crypto Agent** | `agents/crypto-specialist` | Specialist for real-time market data. |
| **Risk Agent** | `agents/risk-analyst` | Specialist for quantitative risk scoring. |
| **MCP Server** | `mcp-server` | External tool bridge for CoinGecko. |

## Tech Stack
- **Framework:** Google ADK (Agent Development Kit) 2.0
- **Communication:** A2A (Agent-to-Agent) & MCP (Model Context Protocol)
- **Deployment:** Docker + Google Cloud Run + Cloud Build
- **Language:** Python 3.14 + uv

## Technical Implementation Details

### Callbacks
The system utilizes lifecycle callbacks for robust operation and observability:
- **Performance Monitoring:** Agents implement `before_agent_callback` and `after_agent_callback` to measure latency and monitor execution performance across the chain.
- **Tool Interception:** Specialist agents use `before_tool_callback` (specifically `on_tool_call`) to intercept and log tool executions along with their computed arguments.

### Memory Management
Agents employ a hybrid memory system to balance persistence and local development needs:
- **Services:** Supports `VertexAiMemoryBankService` for persistent, cross-session memory and `InMemoryMemoryService` as a fallback for local environments.
- **Automatic Selection:** The system automatically selects the appropriate service based on the presence of `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `AGENT_ENGINE_ID` environment variables.

### Communication Protocols
- **Agent-to-Agent (A2A):** Used for seamless orchestration between the Supervisor and specialist agents.
- **Model Context Protocol (MCP):** Leverages `StreamableHTTPConnectionParams` for efficient external tool integration, specifically for the CoinGecko market data bridge.

## Documentation
- **[Agents Deep Dive](./agents/README.md)**: Details on agent logic and inter-agent communication.
- **[Design Spec](./docs/spec.md)**: Original architectural requirements.
