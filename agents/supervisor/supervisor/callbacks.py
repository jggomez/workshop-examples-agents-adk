import time
import logging

from google.adk.agents.callback_context import CallbackContext

logger = logging.getLogger("supervisor")

# Track pipeline start time for total latency (Spec §8)
_pipeline_start_time: float | None = None

APP_NAME = "CryptoRiskArbitrator"


async def before_supervisor(callback_context: CallbackContext) -> None:
    """Spec §8: Start pipeline timer and log agent start."""
    global _pipeline_start_time
    _pipeline_start_time = time.perf_counter()

    # Initialize context variables to prevent KeyError in SequentialAgent instructions
    if "market_data" not in callback_context.state:
        callback_context.state["market_data"] = "Pending market data..."
    if "risk_analysis" not in callback_context.state:
        callback_context.state["risk_analysis"] = "Pending risk analysis..."

    ctx = callback_context
    user_id = ctx.session.user_id

    logger.info(
        "[AGENT_START] -> Entering agent domain: investment_arbitrator | "
        "user=%s",
        user_id,
    )

    context_preview = str(ctx.state.to_dict())[:100]
    logger.info("               Transferred Context: %s...", context_preview)


async def after_supervisor(callback_context: CallbackContext) -> None:
    """Spec §8 + §9.2: Persist session to Memory Bank and log latency.

    Uses callback_context.add_session_to_memory() — the native ADK API
    for Memory Bank integration. This automatically extracts and indexes
    persistent facts from the conversation.
    """
    global _pipeline_start_time
    latency = (
        round(time.perf_counter() - _pipeline_start_time, 3)
        if _pipeline_start_time
        else "N/A"
    )
    _pipeline_start_time = None

    logger.info(
        "[AGENT_COMPLETE] -> investment_arbitrator executed successfully. "
        "Latency: %ss",
        latency,
    )

    # Persist session facts to long-term Memory Bank (Spec §9.2)
    try:
        await callback_context.add_session_to_memory()
        logger.info("[SUPERVISOR] Session persisted to Memory Bank.")
    except Exception as exc:
        logger.error("[SUPERVISOR] Memory persistence failed: %s", exc)
