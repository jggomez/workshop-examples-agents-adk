"""A2A server entry point for the Crypto Specialist agent.

Run locally:
    uv run python server.py

Environment variables:
    PORT            — Server port (default: 8001)
    HOST            — Bind address (default: 0.0.0.0)
    SERVICE_URL     — Public URL for the agent card (default: http://localhost:{PORT})
    MCP_SERVER_URL  — URL of the MCP server (default: Cloud Run production URL)
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

from crypto_specialist import crypto_specialist_agent
from crypto_specialist.memory import memory_service

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)

port = int(os.environ.get("PORT", 8080))
host = os.environ.get("HOST", "0.0.0.0")
service_url = os.environ.get("SERVICE_URL", f"http://localhost:{port}")

# A2A Agent Card — describes this agent's capabilities for discovery
crypto_agent_card = AgentCard(
    name="crypto_specialist",
    url=service_url,
    description=(
        "Real-time cryptocurrency market data specialist. "
        "Retrieves live prices, 24h changes, market cap, and trading volume "
        "for any cryptocurrency via the CoinGecko API through MCP."
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
            "id": "get_crypto_price",
            "name": "Cryptocurrency Price Lookup",
            "description": (
                "Fetches the current market price, 24-hour percentage change, "
                "market capitalization, and trading volume for a specified "
                "cryptocurrency in any fiat or crypto base currency."
            ),
            "tags": ["crypto", "market-data", "prices", "coingecko"],
            "examples": [
                "What is the current price of Bitcoin?",
                "Get Ethereum price in EUR",
                "Show me Solana market data",
            ],
        }
    ],
    default_input_modes=["text/plain"],
    default_output_modes=["text/plain"],
)

# Custom runner to supply our memory_service (Spec §9.2)
custom_runner = Runner(
    app_name=crypto_specialist_agent.name or "crypto_specialist",
    agent=crypto_specialist_agent,
    artifact_service=InMemoryArtifactService(),
    session_service=InMemorySessionService(),
    memory_service=memory_service,
    credential_service=InMemoryCredentialService(),
)

# Convert the ADK agent to a Starlette A2A application
app = to_a2a(
    crypto_specialist_agent,
    host=host,
    port=port,
    agent_card=crypto_agent_card,
    runner=custom_runner,
)

if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)
