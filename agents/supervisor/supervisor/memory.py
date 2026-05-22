import os
import logging
from google.adk.memory import InMemoryMemoryService, VertexAiMemoryBankService

# Initialize logger
logger = logging.getLogger("supervisor")

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


async def get_user_memory(
    app_name: str, user_id: str, query: str = "risk profile and base currency"
) -> list[str]:
    """Search for relevant user facts in the memory bank.

    Returns a list of string facts, or an empty list if no memories are found
    or if the service is unavailable, ensuring the pipeline never crashes.
    """
    try:
        response = await memory_service.search_memory(
            app_name=app_name, user_id=user_id, query=query
        )
        memories = []
        for entry in response.memories:
            if entry.content and entry.content.parts:
                text = " ".join([part.text for part in entry.content.parts if part.text])
                if text:
                    memories.append(text)
        return memories
    except Exception as exc:
        logger.warning("Memory search failed (non-fatal): %s", exc)
        return []
