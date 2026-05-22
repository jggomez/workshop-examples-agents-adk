from google.adk.agents import Agent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types as genai_types

from .callbacks import before_crypto_agent, after_crypto_agent, on_tool_call
from .tools import crypto_toolset

# Crypto Market Specialist Agent (Spec §4.2)
# Dedicated to fetching real-time market data with high precision.
# Does NOT generate financial advice — returns pure structured data.
crypto_specialist_agent = Agent(
    name="crypto_specialist",
    model="gemini-2.5-flash",
    instruction="""
    You are a Real-time Market Data Specialist.
    Your unique goal is to retrieve exact asset quotes using the available tools.

    Rules:
    - ALWAYS use get_crypto_price to fetch the latest data.
    - If the user doesn't specify a currency, read the user's base currency preference from the `<PAST_CONVERSATIONS>` block if present. If not mentioned in past conversations, default to 'usd'.
    - Return ONLY the structured data or a brief confirmation. Do not provide financial advice.
    """,
    description="Fetches real-time cryptocurrency prices and market data.",
    tools=[crypto_toolset, PreloadMemoryTool()],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.2,
        top_p=0.95,
        max_output_tokens=512,
    ),
    before_agent_callback=before_crypto_agent,
    after_agent_callback=after_crypto_agent,
    before_tool_callback=on_tool_call,
    output_key="market_data",
)
