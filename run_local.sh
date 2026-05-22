#!/bin/bash

# Configuration
MCP_PORT=8000
CRYPTO_PORT=8001
RISK_PORT=8002
SUPERVISOR_WEB_PORT=8005

# Function to kill all background processes on exit
cleanup() {
    echo ""
    echo "Stopping all services..."
    # Kill the entire process group to ensure background jobs are terminated
    kill 0
}
trap cleanup EXIT

echo "--------------------------------------------------------"
echo "Starting CryptoRiskArbitrator Local System"
echo "--------------------------------------------------------"

# Check for required environment variables
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY is not set in your environment."
    echo "Please export it: export GOOGLE_API_KEY='your-key'"
    exit 1
fi

# Project defaults for local run
export GOOGLE_CLOUD_PROJECT=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project 2>/dev/null || echo "devhack-3f0c2")}
export GOOGLE_CLOUD_LOCATION=${GOOGLE_CLOUD_LOCATION:-"us-central1"}
export AGENT_ENGINE_ID=${AGENT_ENGINE_ID:-"agents-crypto"}

echo "Using Project: $GOOGLE_CLOUD_PROJECT"

# 1. Start MCP Server
echo "[1/4] Starting MCP Server on port $MCP_PORT..."
cd mcp-server
PORT=$MCP_PORT uv run python server.py > ../mcp_server.log 2>&1 &
cd ..

# 2. Start Risk Analyst
echo "[2/4] Starting Risk Analyst on port $RISK_PORT..."
cd agents/risk-analyst
PORT=$RISK_PORT \
GOOGLE_API_KEY=$GOOGLE_API_KEY \
GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION \
AGENT_ENGINE_ID=$AGENT_ENGINE_ID \
uv run python server.py > ../risk_analyst.log 2>&1 &
cd ../..

# 3. Start Crypto Specialist
echo "[3/4] Starting Crypto Specialist on port $CRYPTO_PORT..."
cd agents/crypto-specialist
PORT=$CRYPTO_PORT \
MCP_SERVER_URL="http://localhost:$MCP_PORT/mcp" \
GOOGLE_API_KEY=$GOOGLE_API_KEY \
GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION \
AGENT_ENGINE_ID=$AGENT_ENGINE_ID \
uv run python server.py > ../crypto_specialist.log 2>&1 &
cd ../..

# Wait a moment for services to initialize
sleep 3

# 4. Start Supervisor Web UI
echo "[4/4] Starting Supervisor Web UI on port $SUPERVISOR_WEB_PORT..."
echo "Access the interface at: http://localhost:$SUPERVISOR_WEB_PORT"
echo "Logs are available in *.log files"
echo "Press Ctrl+C to stop all services"
echo "--------------------------------------------------------"

cd agents/supervisor
CRYPTO_AGENT_URL="http://localhost:$CRYPTO_PORT" \
RISK_AGENT_URL="http://localhost:$RISK_PORT" \
GOOGLE_API_KEY=$GOOGLE_API_KEY \
GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT \
GOOGLE_CLOUD_LOCATION=$GOOGLE_CLOUD_LOCATION \
AGENT_ENGINE_ID=$AGENT_ENGINE_ID \
uv run adk web --port $SUPERVISOR_WEB_PORT supervisor
