import os

from google.adk.agents import Agent, SequentialAgent
from google.adk.agents.remote_a2a_agent import (
    RemoteA2aAgent,
    AGENT_CARD_WELL_KNOWN_PATH,
)
from google.adk.tools.agent_tool import AgentTool
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types as genai_types

from .callbacks import before_supervisor, after_supervisor

# ---------------------------------------------------------------------------
# A2A URLs — configurable via environment variables for local vs production
# ---------------------------------------------------------------------------
CRYPTO_AGENT_URL = os.environ.get("CRYPTO_AGENT_URL", "http://localhost:8001")
RISK_AGENT_URL = os.environ.get("RISK_AGENT_URL", "http://localhost:8002")

# ---------------------------------------------------------------------------
# Remote A2A Agents — proxies to independently deployed specialist services
# ---------------------------------------------------------------------------
remote_crypto_agent = RemoteA2aAgent(
    name="crypto_specialist",
    description="Fetches real-time cryptocurrency prices and market data.",
    agent_card=(
        f"{CRYPTO_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
    use_legacy=False,
)

remote_risk_agent = RemoteA2aAgent(
    name="risk_analyst",
    description="Evaluates financial risk and volatility metrics.",
    agent_card=(
        f"{RISK_AGENT_URL}{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
    use_legacy=False,
)

# This sequence performs the data gathering and risk calculation
sequencer_agent_crypto_analyst = SequentialAgent(
    name="sequencer_agent_crypto_analyst",
    sub_agents=[
        remote_crypto_agent,
        remote_risk_agent,
    ],
    description="Executes the sequential pipeline: Crypto Data -> Risk Analysis.",
)

# ---------------------------------------------------------------------------
# Investment Committee Supervisor (Spec §4.1)
# ---------------------------------------------------------------------------
root_agent = Agent(
    name="root_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are the Director of the Investment Committee for the CryptoRiskArbitrator system.

    ### MISSION
    Your goal is to coordinate a pipeline that fetches crypto market data via the Crypto Specialist and performs quantitative risk evaluation via the Risk Analyst.

    ### OPERATIONAL RULES
    1. **Session Initialization**: 
       - If the user greeting is generic (e.g., 'Hello', 'Hi', 'Hola') and there is no previous context, greet them professionally, explain your role as the Committee Director, and ask which cryptocurrency and currency pair they would like to analyze today.
    
    2. **Input Analysis & Execution**:
       - Analyze the user input. If the user asks for information about a specific cryptocurrency (e.g., 'Analyze Bitcoin', 'Price of ETH'), you MUST call the `sequencer_agent_crypto_analyst` tool immediately to gather data.
       - If the user is just saying hello or asking general questions, introduce yourself and wait for a specific request. DO NOT try to generate a report without real data.

    3. **Report Consolidation**:
       - ONLY when you have valid data returned from the specialists in `{market_data}` and `{risk_analysis}`, consolidate them into a high-fidelity Markdown report.
       - If these variables contain 'Pending' or 'No data', and you haven't called the specialists yet, do so.

    ### DATA RECEIVED (Internal State)
    - Market Data: {market_data}
    - Risk Analysis: {risk_analysis}

    ### FINAL REPORT STRUCTURE (Markdown)
    1. Executive Summary
    2. Market Snapshot
    3. Risk Assessment & Verdict
    4. Strategic Recommendations (Stop-Loss, Entry Points)

    Be professional, elite-level analytical, and concise.
    """,
    tools=[PreloadMemoryTool(), AgentTool(sequencer_agent_crypto_analyst)],
    generate_content_config=genai_types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=2048,
    ),
    before_agent_callback=before_supervisor,
    after_agent_callback=after_supervisor,
)
