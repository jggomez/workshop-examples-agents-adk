import os

from google.adk.tools import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams

# MCP Server URL: configurable via environment variable for local vs production
MCP_SERVER_URL = os.environ.get(
    "MCP_SERVER_URL",
    "https://system-crypto-mcp-server-CHANGE_ME.us-central1.run.app/mcp",
)

# Create the MCP Toolset with tool_filter to expose only relevant tools
crypto_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url=MCP_SERVER_URL,
        timeout=60.0,
    ),
    tool_filter=["get_crypto_price"],
)
