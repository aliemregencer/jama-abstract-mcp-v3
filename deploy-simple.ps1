# JAMA Abstract Generator - Basit Deployment Script

Write-Host "🚀 JAMA Abstract Generator Deployment" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# 1. Git durumunu kontrol et
Write-Host "`n📋 Git durumu kontrol ediliyor..." -ForegroundColor Yellow
try {
    $gitStatus = git status --porcelain 2>&1
    if ($gitStatus) {
        Write-Host "⚠️  Uncommitted changes detected:" -ForegroundColor Yellow
        Write-Host $gitStatus -ForegroundColor White
        Write-Host "`n💡 Önce değişiklikleri commit edin:" -ForegroundColor Cyan
        Write-Host "   git add ." -ForegroundColor White
        Write-Host "   git commit -m 'Deployment için hazırlık'" -ForegroundColor White
        Write-Host "   git push" -ForegroundColor White
    } else {
        Write-Host "✅ Git repository temiz" -ForegroundColor Green
    }
} catch {
    Write-Host "❌ Git kontrol hatası: $_" -ForegroundColor Red
}

# 2. Docker test
Write-Host "`n🐳 Docker test ediliyor..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Docker kurulu: $dockerVersion" -ForegroundColor Green
        
        # Docker build test
        Write-Host "🔨 Docker image build test ediliyor..." -ForegroundColor Yellow
        docker build -t jama-abstract-generator-test . 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Docker build başarılı" -ForegroundColor Green
            # Test image'ı temizle
            docker rmi jama-abstract-generator-test 2>&1 | Out-Null
        } else {
            Write-Host "❌ Docker build hatası" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Docker kurulu değil" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Docker test hatası: $_" -ForegroundColor Red
}

# 3. Local test
Write-Host "`n🧪 Local test ediliyor..." -ForegroundColor Yellow
try {
    $testResult = python -c "import server; print('OK')" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python server import başarılı" -ForegroundColor Green
    } else {
        Write-Host "❌ Python server import hatası" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Local test hatası: $_" -ForegroundColor Red
}

# 4. Deployment seçenekleri
Write-Host "`n🎯 Deployment Seçenekleri:" -ForegroundColor Cyan
Write-Host "1. Smithery.ai Web Interface" -ForegroundColor White
Write-Host "2. GitHub Actions (Otomatik)" -ForegroundColor White
Write-Host "3. Docker Compose (Local)" -ForegroundColor White
Write-Host "4. Manuel Docker" -ForegroundColor White

Write-Host "`n📖 Detaylı bilgi için:" -ForegroundColor Yellow
Write-Host "   - deployment-guide.md dosyasını okuyun" -ForegroundColor White
Write-Host "   - README.md dosyasını inceleyin" -ForegroundColor White

Write-Host "`n🚀 Hızlı başlangıç için:" -ForegroundColor Green
Write-Host "   # Local test:" -ForegroundColor White
Write-Host "   docker-compose up --build" -ForegroundColor White
Write-Host "`n   # Health check:" -ForegroundColor White
Write-Host "   curl http://localhost:8000/health" -ForegroundColor White
