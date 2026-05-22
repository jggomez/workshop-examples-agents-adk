# Risk Analyst Agent

The **Risk Analyst** is an expert agent specializing in quantitative cryptocurrency risk assessment.

## Features
- **Volatility Analysis:** Evaluates the risk profile of specific crypto assets.
- **Risk Scoring:** Generates a normalized risk score (0-10) based on market conditions.
- **Portfolio Protection:** Calculates suggested Stop-Loss thresholds tailored to user profiles (Conservative, Balanced, Aggressive).
- **A2A Protocol:** Fully compatible with the Agent-to-Agent protocol for seamless integration into larger workflows.

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
