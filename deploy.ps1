# JAMA Abstract Generator MCP Server - Smithery Deployment Script (PowerShell)

Write-Host "🚀 Starting deployment to Smithery..." -ForegroundColor Green

# Check if smithery CLI is installed
try {
    $null = Get-Command smithery -ErrorAction Stop
    Write-Host "✅ Smithery CLI is installed" -ForegroundColor Green
} catch {
    Write-Host "❌ Smithery CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   npm install -g @smithery/cli" -ForegroundColor Yellow
    exit 1
}

# Check if logged in to Smithery
try {
    $status = smithery list servers 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Not logged in"
    }
    Write-Host "✅ Logged in to Smithery" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Smithery first:" -ForegroundColor Yellow
    Write-Host "   smithery login" -ForegroundColor Yellow
    Write-Host "   Get your API key from: https://smithery.ai/account/api-keys" -ForegroundColor Yellow
    exit 1
}

# Build the MCP server using the config file
Write-Host "🔨 Building MCP server..." -ForegroundColor Green
try {
    smithery build smithery.config.js
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Build failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Build failed: $_" -ForegroundColor Red
    exit 1
}

# Run the server (this will deploy it to Smithery)
Write-Host "🚀 Deploying to Smithery..." -ForegroundColor Green
try {
    Write-Host "Starting server with tunnel..." -ForegroundColor Yellow
    smithery dev smithery.config.js
} catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔗 Your MCP server is now running on Smithery!" -ForegroundColor Cyan
Write-Host "📋 You can monitor it using: smithery list servers" -ForegroundColor Cyan
Write-Host "🔧 To stop the server, press Ctrl+C" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 To use this MCP server, add it to your MCP client configuration:" -ForegroundColor Yellow
Write-Host "   - name: jama-abstract-generator" -ForegroundColor White
Write-Host "     transport: smithery" -ForegroundColor White
Write-Host "     config:" -ForegroundColor White
Write-Host "       project: [YOUR_SMITHERY_PROJECT_ID]" -ForegroundColor White
