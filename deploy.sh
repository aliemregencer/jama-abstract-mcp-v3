#!/bin/bash

# JAMA Abstract Generator MCP Server - Smithery Deployment Script

set -e

echo "🚀 Starting deployment to Smithery..."

# Check if smithery CLI is installed
if ! command -v smithery &> /dev/null; then
    echo "❌ Smithery CLI is not installed. Please install it first:"
    echo "   npm install -g @smithery/cli"
    exit 1
fi

# Check if logged in to Smithery
if ! smithery auth status &> /dev/null; then
    echo "🔐 Please login to Smithery first:"
    echo "   smithery auth login"
    exit 1
fi

# Build and deploy
echo "📦 Building and deploying to Smithery..."

# Deploy using smithery.yaml configuration
smithery deploy --config smithery.yaml

echo "✅ Deployment completed successfully!"
echo ""
echo "🔗 Your MCP server is now available on Smithery"
echo "📋 You can monitor it using: smithery status"
echo "📊 View logs using: smithery logs"
echo ""
echo "🎯 To use this MCP server, add it to your MCP client configuration:"
echo "   - name: jama-abstract-generator"
echo "     transport: smithery"
echo "     config:"
echo "       project: [YOUR_SMITHERY_PROJECT_ID]"
