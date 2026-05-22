import time
import logging

from google.adk.agents.callback_context import CallbackContext
from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

logger = logging.getLogger("risk_analyst")

# Track agent start times for latency measurement (Spec §8)
_start_time: float | None = None


async def before_risk_agent(callback_context: CallbackContext) -> None:
    """Spec §8: on_agent_start — log entry with context preview and start timer."""
    global _start_time
    _start_time = time.perf_counter()

    ctx = callback_context
    logger.info(
        "[AGENT_START] -> Entering agent domain: risk_analyst | "
        "session=%s",
        ctx.session.id,
    )

    context_preview = str(ctx.state.to_dict())[:100]
    logger.info("               Transferred Context: %s...", context_preview)


async def after_risk_agent(callback_context: CallbackContext) -> None:
    """Spec §8: on_agent_complete — log success with latency measurement."""
    global _start_time
    latency = round(time.perf_counter() - _start_time, 3) if _start_time else "N/A"
    _start_time = None

    logger.info(
        "[AGENT_COMPLETE] -> risk_analyst executed successfully. Latency: %ss",
        latency,
    )


async def on_tool_call(
    tool: BaseTool, args: dict, tool_context: ToolContext
) -> dict | None:
    """Spec §8: on_tool_execution — intercept and log tool calls with arguments."""
    logger.info("   [TOOL_CALL] -> Intercepting execution for tool: '%s'", tool.name)
    logger.info("                  Computed Arguments: %s", args)
    return None  # Continue normal execution
