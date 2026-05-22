from google.adk.agents import Agent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types as genai_types

from .callbacks import before_risk_agent, after_risk_agent, on_tool_call
from .tools import calculate_risk_metrics

# Risk Analytics Agent (Spec §4.3)
# Responsible for quantitative analysis, volatility evaluation, and risk verdict.
# Uses a deterministic internal Python tool — no external API calls.
risk_analyst_agent = Agent(
    name="risk_analyst",
    model="gemini-2.5-flash",
    instruction="""
    You are a Quantitative Risk Analyst.
    Your objective is to evaluate volatility and capital exposure based on provided market data.

    Rules:
    - Use the calculate_risk_metrics tool to get objective risk data.
    - Read the user's risk profile preference (which can be 'aggressive', 'conservative', or 'balanced') from the `<PAST_CONVERSATIONS>` block if present. If not mentioned in past conversations, default to 'balanced'.
    - Provide a clear verdict (Low, Medium, High) and explain the Stop-Loss levels.
    - Be concise and purely analytical.
    """,
    description="Evaluates financial risk and volatility metrics.",
    tools=[calculate_risk_metrics, PreloadMemoryTool()],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        max_output_tokens=1024,
    ),
    before_agent_callback=before_risk_agent,
    after_agent_callback=after_risk_agent,
    before_tool_callback=on_tool_call,
    output_key="risk_analysis",
)

