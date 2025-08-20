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
if ! smithery list servers &> /dev/null; then
    echo "🔐 Please login to Smithery first:"
    echo "   smithery login"
    echo "   Get your API key from: https://smithery.ai/account/api-keys"
    exit 1
fi

# Build the MCP server
echo "🔨 Building MCP server..."
if smithery build server.py; then
    echo "✅ Build completed successfully!"
else
    echo "❌ Build failed"
    exit 1
fi

# Run the server (this will deploy it to Smithery)
echo "🚀 Deploying to Smithery..."
echo "Starting server with tunnel..."
smithery dev server.py

echo "✅ Deployment completed successfully!"
echo ""
echo "🔗 Your MCP server is now running on Smithery!"
echo "📋 You can monitor it using: smithery list servers"
echo "🔧 To stop the server, press Ctrl+C"
echo ""
echo "🎯 To use this MCP server, add it to your MCP client configuration:"
echo "   - name: jama-abstract-generator"
echo "     transport: smithery"
echo "     config:"
echo "       project: [YOUR_SMITHERY_PROJECT_ID]"
