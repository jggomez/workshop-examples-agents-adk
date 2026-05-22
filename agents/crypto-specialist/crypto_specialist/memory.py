import os
import logging
from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService

# Initialize logger
logger = logging.getLogger("crypto_specialist")

# Configure memory service based on environment variables
project = os.environ.get("GOOGLE_CLOUD_PROJECT")
location = os.environ.get("GOOGLE_CLOUD_LOCATION")
agent_engine_id = os.environ.get("AGENT_ENGINE_ID")

if project and location and agent_engine_id:
    logger.info(
        "Initializing VertexAiMemoryBankService with Project: %s, Location: %s, Engine ID: %s",
        project,
        location,
        agent_engine_id,
    )
    memory_service = VertexAiMemoryBankService(
        project=project, location=location, agent_engine_id=agent_engine_id
    )
else:
    logger.warning(
        "Missing memory bank environment variables (GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION, AGENT_ENGINE_ID). "
        "Falling back to InMemoryMemoryService."
    )
    memory_service = InMemoryMemoryService()
