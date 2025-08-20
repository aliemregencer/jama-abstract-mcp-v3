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
    $status = smithery auth status 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Not logged in"
    }
    Write-Host "✅ Logged in to Smithery" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Smithery first:" -ForegroundColor Yellow
    Write-Host "   smithery auth login" -ForegroundColor Yellow
    exit 1
}

# Build and deploy
Write-Host "📦 Building and deploying to Smithery..." -ForegroundColor Green

# Deploy using smithery.yaml configuration
try {
    smithery deploy --config smithery.yaml
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Deployment completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Deployment failed" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Deployment failed: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🔗 Your MCP server is now available on Smithery" -ForegroundColor Cyan
Write-Host "📋 You can monitor it using: smithery status" -ForegroundColor Cyan
Write-Host "📊 View logs using: smithery logs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🎯 To use this MCP server, add it to your MCP client configuration:" -ForegroundColor Yellow
Write-Host "   - name: jama-abstract-generator" -ForegroundColor White
Write-Host "     transport: smithery" -ForegroundColor White
Write-Host "     config:" -ForegroundColor White
Write-Host "       project: [YOUR_SMITHERY_PROJECT_ID]" -ForegroundColor White
