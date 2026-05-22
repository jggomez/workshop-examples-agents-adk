# Risk Analyst Agent

The **Risk Analyst** is an expert agent specializing in quantitative cryptocurrency risk assessment.

## Features
- **Volatility Analysis:** Evaluates the risk profile of specific crypto assets.
- **Risk Scoring:** Generates a normalized risk score (0-10) based on market conditions.
- **Portfolio Protection:** Calculates suggested Stop-Loss thresholds tailored to user profiles (Conservative, Balanced, Aggressive).
- **A2A Protocol:** Fully compatible with the Agent-to-Agent protocol for seamless integration into larger workflows.

## Technical Details

### Memory Management
The analyst utilizes a hybrid memory system to maintain risk evaluation context:
- **Persistent Memory:** Uses `VertexAiMemoryBankService` for cross-session asset risk history.
- **Local Fallback:** Uses `InMemoryMemoryService` for development and testing.
- **Auto-Provisioning:** Services are automatically selected based on `GOOGLE_CLOUD_PROJECT`, `GOOGLE_CLOUD_LOCATION`, and `AGENT_ENGINE_ID`.

### Callbacks & Performance
- **Lifecycle Hooks:** Implements `before_agent_callback` and `after_agent_callback` to measure calculation latency and execution efficiency.
- **Execution Logging:** Uses `before_tool_callback` (`on_tool_call`) to log the arguments used for quantitative analysis tools.

### Communication
- **A2A Orchestration:** Fully integrated via the Agent-to-Agent protocol, enabling the Supervisor to delegating quantitative tasks.

## Configuration
The agent requires the following environment variables:
- `GOOGLE_API_KEY`: Your Gemini API key.

## Local Development
```bash
# Install dependencies
uv sync

# Run the A2A server
GOOGLE_API_KEY="your-key" uv run python server.py
```

## Deployment
This agent is deployed as a managed service on Google Cloud Run.
