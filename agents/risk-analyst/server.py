"""A2A server entry point for the Risk Analyst agent.

Run locally:
    uv run python server.py

Environment variables:
    PORT            — Server port (default: 8002)
    HOST            — Bind address (default: 0.0.0.0)
    SERVICE_URL     — Public URL for the agent card (default: http://localhost:{PORT})
    GOOGLE_API_KEY  — Gemini API key (required)
"""

import os
import logging

import uvicorn
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from a2a.types import AgentCard
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.runners import Runner
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService

from risk_analyst import risk_analyst_agent
from risk_analyst.memory import memory_service

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)

port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")
service_url = os.environ.get("SERVICE_URL", f"http://localhost:{port}")

# A2A Agent Card — describes this agent's capabilities for discovery
risk_agent_card = AgentCard(
    name="risk_analyst",
    url=service_url,
    description=(
        "Quantitative risk analyst specializing in cryptocurrency volatility. "
        "Computes risk scores, expected drawdowns, and Stop-Loss thresholds "
        "adjusted to conservative, balanced, or aggressive investor profiles."
    ),
    version="1.0.0",
    provider={
        "organization": "Crypto Risk Arbitrator",
        "url": "https://github.com/jggomez/workshop-agents-mayo",
    },
    capabilities={
        "streaming": False,
        "pushNotifications": False,
        "stateTransitionHistory": False,
    },
    skills=[
        {
            "id": "calculate_risk_metrics",
            "name": "Risk Metrics Calculator",
            "description": (
                "Computes a normalized risk score (0-10), risk classification "
                "(Low/Moderate/High), expected 24h drawdown, and suggested "
                "Stop-Loss level based on current price and user risk profile."
            ),
            "tags": ["risk", "volatility", "stop-loss", "portfolio"],
            "examples": [
                "Evaluate risk for Bitcoin at $67,000",
                "Calculate risk with aggressive profile",
                "What is the Stop-Loss for ETH at $3,200 with conservative profile?",
            ],
        }
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
)

# Custom runner to supply our memory_service (Spec §9.2)
custom_runner = Runner(
    app_name=risk_analyst_agent.name or "risk_analyst",
    agent=risk_analyst_agent,
    artifact_service=InMemoryArtifactService(),
    session_service=InMemorySessionService(),
    memory_service=memory_service,
    credential_service=InMemoryCredentialService(),
)

# Convert the ADK agent to a Starlette A2A application
app = to_a2a(
    risk_analyst_agent,
    host=host,
    port=port,
    agent_card=risk_agent_card,
    runner=custom_runner,
)

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
