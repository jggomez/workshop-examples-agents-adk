# Agent System

This directory contains the independent AI agents that form the **Crypto Risk Arbitrator** ecosystem.

## Architecture & Communication
The system follows a hub-and-spoke architecture where the **Supervisor** coordinates specialized "workers" using the **Agent-to-Agent (A2A)** protocol.

- **[Supervisor](./supervisor)**: The entry point and orchestrator.
- **[Crypto Specialist](./crypto-specialist)**: Data retrieval and market analysis.
- **[Risk Analyst](./risk-analyst)**: Quantitative risk scoring and portfolio advice.

## Multi-Agent Workflow
1.  **Request:** User asks for an investment analysis.
2.  **Discovery:** Supervisor identifies necessary skills.
3.  **A2A Call (1):** Supervisor requests market data from the Crypto Specialist.
4.  **A2A Call (2):** Supervisor sends market data to the Risk Analyst for evaluation.
5.  **Synthesis:** Supervisor combines all inputs into a final recommendation.

## Independent Scalability
Each agent is a self-contained Python project with its own:
- `pyproject.toml` (Dependencies)
- `Dockerfile` (Environment)
- `cloudbuild.yaml` (CI/CD)

This allows you to update or scale individual agents without affecting the rest of the system.

## Common Implementation Features

### Hybrid Memory System
All agents in the ecosystem support a hybrid memory management strategy:
- **Persistence:** Uses `VertexAiMemoryBankService` for persistent, cross-session memory in production environments.
- **Development:** Falls back to `InMemoryMemoryService` for local development.
- **Auto-Config:** Selection is automatically handled based on the environment variables `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `AGENT_ENGINE_ID`.

### Lifecycle Callbacks
Standardized callbacks are used across the system for performance and logging:
- **Agent Monitoring:** `before_agent_callback` and `after_agent_callback` are used for performance monitoring and latency measurement.
- **Tool Interception:** Specialist agents leverage `before_tool_callback` (via `on_tool_call`) to intercept and log tool executions and their computed arguments.
