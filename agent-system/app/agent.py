"""Cryptocurrency Analysis Pipeline — 3-agent sequential system.

Pipeline:
  1. crypto_price_agent   → fetches price via MCP, stores in state["crypto-value"]
  2. market_research_agent → researches market via Google Search, stores in state["instigation-result"]
  3. report_agent          → reads both state keys, produces a formal report
"""

from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

# ---------------------------------------------------------------------------
# MCP connection — Streamable HTTP transport
# ---------------------------------------------------------------------------
MCP_SERVER_URL = (
    "https://system-crypto-mcp-server-823002731253.us-central1.run.app/mcp"
)

crypto_mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=MCP_SERVER_URL),
)

# ---------------------------------------------------------------------------
# Agent 1 — Crypto Price Agent
# ---------------------------------------------------------------------------
PRICE_AGENT_INSTRUCTION = """\
You are a cryptocurrency price assistant.

## Your task
Use the `get_crypto_price` tool to retrieve the current price of the
cryptocurrency the user asks about.

## Rules
1. **Always use the tool** — never guess or invent prices.
2. Map common names/tickers to CoinGecko slugs before calling the tool:
   BTC → bitcoin, ETH → ethereum, SOL → solana, ADA → cardano,
   DOGE → dogecoin, XRP → ripple, DOT → polkadot, AVAX → avalanche-2,
   MATIC → matic-network, LINK → chainlink.
3. After getting the result, output a clear summary with the crypto name,
   its current price, and the currency.
4. If the tool returns an error, say so clearly.
5. Respond in the **same language** the user writes in.
"""

crypto_price_agent = Agent(
    name="crypto_price_agent",
    model="gemini-2.5-flash",
    instruction=PRICE_AGENT_INSTRUCTION,
    tools=[crypto_mcp_toolset],
    output_key="crypto-value",
)

# ---------------------------------------------------------------------------
# Agent 2 — Market Research Agent
# ---------------------------------------------------------------------------
RESEARCH_AGENT_INSTRUCTION = """\
You are a cryptocurrency market research analyst.

## Your task
The previous agent already fetched the price of a cryptocurrency.
That information is available here: {crypto-value}

Using Google Search, investigate the **current market status** of that
same cryptocurrency.  Focus on:
- Recent news and events affecting the price.
- Market sentiment (bullish, bearish, neutral).
- Key technical or fundamental factors.
- Any upcoming events (halvings, upgrades, regulations).

## Rules
1. Base your research on the cryptocurrency identified in {crypto-value}.
2. Provide a structured summary of your findings.
3. Respond in the **same language** the user writes in.
"""

market_research_agent = Agent(
    name="market_research_agent",
    model="gemini-2.5-flash",
    instruction=RESEARCH_AGENT_INSTRUCTION,
    tools=[google_search],
    output_key="instigation-result",
)

# ---------------------------------------------------------------------------
# Agent 3 — Report Agent
# ---------------------------------------------------------------------------
REPORT_AGENT_INSTRUCTION = """\
You are a professional financial report writer specialising in cryptocurrencies.

## Your task
Produce a **formal report** about the current state of the cryptocurrency,
combining the data provided by the previous agents:

- **Price data**: {crypto-value}
- **Market research**: {instigation-result}

## Report structure
1. **Executive Summary** — one-paragraph overview.
2. **Current Price** — present the price data clearly.
3. **Market Analysis** — summarise the research findings: news, sentiment,
   key factors.
4. **Outlook** — short-term perspective based on the research.
5. **Disclaimer** — remind the reader this is not financial advice.

## Rules
1. Use a professional, formal tone.
2. Do NOT call any tools — just synthesise the information already provided.
3. Respond in the **same language** the user writes in.
"""

report_agent = Agent(
    name="report_agent",
    model="gemini-2.5-flash",
    instruction=REPORT_AGENT_INSTRUCTION,
)

# ---------------------------------------------------------------------------
# Root agent — Sequential Pipeline
# ---------------------------------------------------------------------------
root_agent = SequentialAgent(
    name="crypto_analysis_pipeline",
    sub_agents=[crypto_price_agent, market_research_agent, report_agent],
)
