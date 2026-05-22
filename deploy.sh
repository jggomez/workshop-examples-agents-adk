#!/bin/bash
set -e

# Configuration
REGION="us-central1"
PROJECT_ID=$(gcloud config get-value project)
AGENTS_REPO="agents-repo"
MCP_REPO="mcp-repo"

echo "Using Project ID: $PROJECT_ID"
echo "Region: $REGION"

# 1. Ensure Artifact Registry repositories exist
echo "Ensuring Artifact Registry repositories exist..."
gcloud artifacts repositories create $AGENTS_REPO \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for AI Agents" || true

gcloud artifacts repositories create $MCP_REPO \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker repository for MCP Servers" || true

# Check for required environment variables
if [ -z "$GOOGLE_API_KEY" ]; then
    echo "Error: GOOGLE_API_KEY is not set in your environment."
    exit 1
fi

# 2. Deploy MCP Server
echo "Building and deploying MCP Server..."
cd mcp-server
gcloud builds submit --config cloudbuild.yaml --substitutions=_ARTIFACT_REGISTRY_REPO="$REGION-docker.pkg.dev/$PROJECT_ID/$MCP_REPO",_DEPLOY_REGION="$REGION"
MCP_URL=$(gcloud run services describe system-crypto-mcp-server --region "$REGION" --format 'value(status.url)')/mcp
cd ..

echo "MCP Server URL: $MCP_URL"

# 3. Deploy Risk Analyst
echo "Building and deploying Risk Analyst..."
cd agents/risk-analyst
gcloud builds submit --config cloudbuild.yaml --substitutions=_AR_REPO="$REGION-docker.pkg.dev/$PROJECT_ID/$AGENTS_REPO",_DEPLOY_REGION="$REGION",_GOOGLE_API_KEY="$GOOGLE_API_KEY"
RISK_URL=$(gcloud run services describe risk-analyst --region "$REGION" --format 'value(status.url)')
cd ../..

echo "Risk Analyst URL: $RISK_URL"

# 4. Deploy Crypto Specialist (depends on MCP_URL)
echo "Building and deploying Crypto Specialist..."
cd agents/crypto-specialist
gcloud builds submit --config cloudbuild.yaml --substitutions=_AR_REPO="$REGION-docker.pkg.dev/$PROJECT_ID/$AGENTS_REPO",_DEPLOY_REGION="$REGION",_MCP_SERVER_URL="$MCP_URL",_GOOGLE_API_KEY="$GOOGLE_API_KEY"
CRYPTO_URL=$(gcloud run services describe crypto-specialist --region "$REGION" --format 'value(status.url)')
cd ../..

echo "Crypto Specialist URL: $CRYPTO_URL"

# 5. Deploy Supervisor (depends on Specialist URLs)
echo "Building and deploying Supervisor..."
cd agents/supervisor
gcloud builds submit --config cloudbuild.yaml --substitutions=_AR_REPO="$REGION-docker.pkg.dev/$PROJECT_ID/$AGENTS_REPO",_DEPLOY_REGION="$REGION",_CRYPTO_AGENT_URL="$CRYPTO_URL",_RISK_AGENT_URL="$RISK_URL",_GOOGLE_API_KEY="$GOOGLE_API_KEY"
SUPERVISOR_URL=$(gcloud run services describe supervisor --region "$REGION" --format 'value(status.url)')
cd ../..

echo "--------------------------------------------------------"
echo "System Deployment Complete!"
echo "Supervisor URL: $SUPERVISOR_URL"
echo "--------------------------------------------------------"
