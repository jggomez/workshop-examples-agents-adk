# Technical Specification: Multi-Agent Crypto & Risk Arbitration System

## 1. Purpose and Goals (Expert Agentic AI Alignment)

### What

This specification outlines a high-efficiency investment arbitration and financial risk evaluation framework structured under a hierarchical **Multi-Agent System (MAS)** pattern. Utilizing the official Google **Agent Development Kit (ADK)**, it coordinates three autonomous, decoupled entities: an Investment Supervisor, a Crypto Market Specialist, and a Technical Risk Analyst.

### Why

* **Separation of Concerns:** Isolating stochastic I/O data acquisition from deterministic quantitative mathematical analysis minimizes hallucination rates and optimizes context window usage.
* **Context Efficiency:** Instead of injecting every tool into a single monolithic context—which causes attention degradation—each agent operates exclusively with the tools required for its immediate sub-task.
* **Autonomous Goal Decomposition:** The system applies a structured Chain-of-Thought approach where the user's high-level financial intent is translated into granular, executable agent tasks without manual developer hardcoding.

---

## 2. Technical Stack

* **Runtime Environment:** Python 3.11+
* **Dependency Management:** `uv` (Fast Python package installer and resolver to guarantee immediate, reproducible environments).
* **Core SDK:** Google ADK (Agent Development Kit).
* **Tool Infrastructure:** Model Context Protocol (MCP) Server for real-time, streamable financial data ingestion via streamable-HTTP.
* **Long-Term Memory Layer:** Google ADK Native `Memory Bank` Architecture.

---

## 3. Multi-Agent System Description

The system implements a **Supervisor-Workers** design pattern. The execution flow is strictly synchronous, deterministic, and top-down during the data-gathering phase, and consolidated during the final orchestration phase.

```
                  +-----------------------+
                  |  Investment Supervisor| <--- (User Request)
                  +-----------+-----------+
                              |
         +--------------------+--------------------+
         | (A2A Request)                           | (A2A Request + Market Data)
         v                                         v
+------------------+                      +------------------+
| Crypto Specialist|                      |   Risk Analyst   |
+--------+---------+                      +--------+---------+
         |                                         |
         v (Async Tool Call)                       v (Sync Tool Call)
   [MCP Server]                             [Internal Python Tool]
(get_crypto_price)                        (calculate_risk_metrics)

```

1. **Ingestion Phase:** The Supervisor receives and semantically interprets the user's investment objective.
2. **A2A Orchestration Phase (Step 1):** The Supervisor delegates data extraction to the *Crypto Specialist*, transferring execution control.
3. **Data Fetching Phase (MCP):** The *Crypto Specialist* executes the pre-existing, streaming-compatible tool connected to the MCP server and returns the raw structured financial payload.
4. **A2A Orchestration Phase (Step 2):** The Supervisor receives the market data, enriches the session state, and forwards the aggregated context to the *Risk Analyst*.
5. **Local Computation Phase:** The *Risk Analyst* processes the data through a deterministic, internal analytical tool and emits a volatility verdict.
6. **Consolidation Phase:** The Supervisor unifies both context blocks and generates the final high-fidelity executive report.

---

## 4. Agent and Tool Descriptions

### 4.1. Investment Committee Supervisor

* **System Instruction:** Acts as the Director of the Investment Committee. Its sole objective is to coordinate the pipeline's execution, decompose the user's request, sequentially invoke specialist agents via A2A protocols, and format the final deliverable into clean Markdown.
* **Tools:** None direct (Delegates all operational tasks).

### 4.2. Crypto Market Specialist

* **System Instruction:** Real-time data specialist. Its unique goal is to interact with the MCP server to retrieve exact asset quotes. It does not generate investment interpretations or financial advice; it returns pure, structured data.
* **Tools:** `get_crypto_price` (External/MCP Tool).

### 4.3. Risk Analytics Agent

* **System Instruction:** Quantitative portfolio analyst. Its objective is to evaluate volatility, capital exposure, and emit a risk verdict (Low, Medium, High) accompanied by clear mitigation guidelines (Stop-Loss levels).
* **Tools:** `calculate_risk_metrics` (Internal/Native Python Tool).

---

## 5. Tool Specifications

### 5.1. Pre-existing External Tool (Asynchronous/MCP/Streamable-HTTP)

This tool interacts directly with the existing MCP server infrastructure and supports streaming protocols.

```python
async def get_crypto_price(crypto_id: str, vs_currency: str = "usd") -> dict:
    """
    Queries the MCP server via streamable-HTTP to fetch the current spot price 
    and market metrics of a cryptocurrency against a specific fiat currency.
    
    Args:
        crypto_id: Identifier of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
        vs_currency: Target fiat currency for comparison (e.g., 'usd', 'mxn').
    """
    # Pre-existing implementation within the MCP server environment
    pass

```

### 5.2. Internal Tool (Synchronous)

A deterministic mathematical calculation tool used to execute local, high-precision code.

```python
def calculate_risk_metrics(current_price: float, risk_profile: str = "balanced") -> dict:
    """
    Mathematically computes the risk index, implicit volatility, and 
    suggested Stop-Loss thresholds based on current market price and user profile.
    
    Args:
        current_price: The active asset price retrieved from the market.
        risk_profile: User risk tolerance ('conservative', 'balanced', 'aggressive').
    """
    volatility_factor = 0.085 if risk_profile == "aggressive" else 0.042
    expected_drawdown = current_price * volatility_factor
    stop_loss_level = current_price * (1 - (volatility_factor * 1.5))
    
    return {
        "risk_score": 8.2 if risk_profile == "aggressive" else 5.4,
        "classification": "High Volatility Asset" if volatility_factor > 0.05 else "Moderate Asset",
        "expected_24h_drawdown": round(expected_drawdown, 2),
        "suggested_stop_loss": round(stop_loss_level, 2)
    }

```

---

## 6. Agent-to-Agent (A2A) Protocol

The Google ADK manages A2A communication through **Structured Context Passing via Session Memory Injection**.

The Supervisor maintains the master conversational state and exposes specific sub-contexts to each worker agent using isolated execution parameters:

```python
# Core runtime protocol flow:
# 1. Supervisor receives user input.
# 2. Supervisor invokes the Crypto Agent, injecting the specific worker instructions.
crypto_output = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Extract current market data for {user_target_crypto}",
    config=types.GenerateContentConfig(system_instruction=crypto_agent_instruction, tools=[get_crypto_price])
)

# 3. Supervisor captures output, appends it to the Risk Agent payload.
risk_output = client.models.generate_content(
    model=MODEL_ID,
    contents=f"Evaluate investment risks using this market payload: {crypto_output.text}",
    config=types.GenerateContentConfig(system_instruction=risk_agent_instruction, tools=[calculate_risk_metrics])
)

```

---

## 7. Model Configurations and Hyperparameters

To ensure deterministic execution behavior and reliable error boundaries, calls are handled under strict parameters utilizing `gemini-2.5-flash`.

```python
from google.api_core import retry

MODEL_ID = "gemini-2.5-flash"

# Agent behavior configuration
agent_config = types.GenerateContentConfig(
    temperature=0.2,  # Low temperature ensures precision in Tool Calling and structured schemas
    top_p=0.95,
    max_output_tokens=1024
)

# Robust execution wrapper with automatic retries for rate limits or 5xx anomalies
def safe_execute_agent_call(prompt: str, config_agent: types.GenerateContentConfig):
    return client.models.generate_content(
        model=MODEL_ID,
        contents=prompt,
        config=config_agent,
        # Exponential backoff retry protocol to mitigate live API exceptions
        retry=retry.Retry(initial=1.0, maximum=10.0, multiplier=2.0)
    )

```

> **Hyperparameter Architecture Note:** The native boundary for temperature parameters in the Gemini model architecture is strictly capped between `0.0` and `2.0`. Attempting to force an out-of-bounds temperature value such as `2.5` breaks the transformer's softmax function and will trigger an immediate HTTP 400 Bad Request error from the API gateway. This specification enforces an analytical default of `0.2` for tool operations, scaling up to `0.7` exclusively for the Supervisor's final editorial synthesis.

---

## 8. Observability Architecture: ADK Callbacks

To stream the agent's internal execution tree directly to the runtime console during execution, lifecycle callback hooks are bound to the operational pipeline:

```python
# Agentic lifecycle event monitoring
def on_agent_start(agent_name: str, context: str):
    print(f"\n[AGENT_START] -> Entering agent domain: {agent_name}")
    print(f"               Transferred Context: {context[:100]}...")

def on_tool_execution(tool_name: str, arguments: dict):
    print(f"   [TOOL_CALL] -> Intercepting execution for tool: '{tool_name}'")
    print(f"                  Computed Arguments: {arguments}")

def on_agent_complete(agent_name: str, latency: float):
    print(f"[AGENT_COMPLETE] -> {agent_name} executed successfully. Latency: {latency}s\n")

```

---

## 9. Memory Management Strategy

The runtime partitions information storage into two separate cognitive layers following the official Google ADK specifications:

### 9.1. Short-Term Memory

* **Mechanism:** Managed through active message history within the current execution thread (`Session Thread`).
* **Functional Goal:** Retains immediate data states between collaborating agents during the active session lifecycle. This ensures the Supervisor preserves the specific market rates delivered by the Crypto Specialist while waiting for the Risk Analyst's execution frame. It is entirely purged upon pipeline completion.

### 9.2. Long-Term Memory (Google ADK Memory Bank)

* **Mechanism:** Implemented using the native **Google ADK Memory Bank** protocol (`[https://adk.dev/sessions/memory/#memory-bank](https://adk.dev/sessions/memory/#memory-bank)`). The system initializes a persistent, structured memory bank attached to the user session identity.
* **Functional Goal:** Automatically extracts, indexes, and stores persistent facts and user preferences (e.g., historical risk profiles like *aggressive* or preferred base currencies like *USD*) across disjointed sessions.
* **Lifecycle Integration:** Before starting the execution pipeline, the Supervisor requests a read-access lock on the active `MemoryBank`. The ADK injects the extracted user context directly into the initialization prompt, enabling personalized risk evaluation without requiring manual re-entry or repetitive data polling. New facts learned during the conversation are continuously committed back to the memory bank asynchronously.