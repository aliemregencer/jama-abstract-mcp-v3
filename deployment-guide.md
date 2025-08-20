# Smithery.ai Deployment Guide

## 🚀 Deployment Yöntemleri

### 1. Web Interface ile Deployment (Önerilen)

1. **Smithery.ai'ye giriş yapın**
   - https://smithery.ai adresine gidin
   - GitHub ile giriş yapın

2. **Yeni proje oluşturun**
   - "New Project" butonuna tıklayın
   - Proje adı: `jama-abstract-generator`
   - Description: "JAMA Network makale URL'sinden görsel özet içeren PowerPoint dosyası oluşturan MCP server"

3. **GitHub repository'yi bağlayın**
   - GitHub repository URL'sini girin
   - Branch: `main` veya `master`

4. **Build konfigürasyonu**
   - Build Command: `docker build -t jama-abstract-generator .`
   - Dockerfile: `Dockerfile` (otomatik tespit edilecek)

5. **Environment variables**
   ```
   PYTHONPATH=/app
   PYTHONUNBUFFERED=1
   JAMA_TEMPLATE=templates/abstract.pptx
   OUTPUT_DIR=outputs
   ```

6. **Port ve health check**
   - Port: `8000`
   - Health check path: `/health` (opsiyonel)

7. **Deploy edin**
   - "Deploy" butonuna tıklayın
   - Build tamamlanana kadar bekleyin

### 2. GitHub Actions ile Otomatik Deployment

1. **Repository secrets ekleyin**
   - `SMITHERY_API_KEY`: Smithery.ai'den alınan API key

2. **GitHub Actions workflow'u çalıştırın**
   - `.github/workflows/deploy-smithery.yml` dosyası otomatik olarak çalışacak

### 3. CLI ile Deployment (Alternatif)

```bash
# Smithery CLI kurulumu
npm install -g @smithery/cli

# Giriş yapın
smithery login

# Proje oluşturun
smithery projects create jama-abstract-generator

# Deploy edin
smithery deploy --project jama-abstract-generator
```

## 🔧 Konfigürasyon Dosyaları

### Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN mkdir -p outputs templates
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV JAMA_TEMPLATE=templates/abstract.pptx
ENV OUTPUT_DIR=outputs
EXPOSE 8000
CMD ["python", "-m", "server"]
```

### requirements.txt
```
fastmcp>=0.9.0
requests>=2.31.0
beautifulsoup4>=4.12.3
lxml>=5.2.2
python-pptx>=0.6.21
aiofiles>=23.2.1
```

## 📋 Deployment Sonrası

### 1. Status Kontrolü
- Smithery dashboard'da proje durumunu kontrol edin
- Logs'ları inceleyin

### 2. MCP Client Konfigürasyonu
```yaml
# MCP client config
- name: jama-abstract-generator
  transport: smithery
  config:
    project: jama-abstract-generator
    api_key: YOUR_SMITHERY_API_KEY
```

### 3. Test Etme
```python
# Test script
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async with stdio_client(StdioServerParameters(
    command="python", 
    args=["-m", "server"]
)) as (read, write):
    async with ClientSession(read, write) as session:
        # Test scrape_jama_article
        result = await session.call_tool(
            "scrape_jama_article",
            {"url": "https://jamanetwork.com/journals/jama/fullarticle/..."}
        )
        print(result)
```

## 🚨 Troubleshooting

### Build Hataları
- Dockerfile syntax kontrolü
- Requirements.txt dependency çakışmaları
- Python version uyumsuzluğu

### Runtime Hataları
- Environment variables eksikliği
- File permissions
- Network connectivity

### MCP Connection Hataları
- Server başlatma hatası
- Tool registration problemi
- Schema validation hatası

## 📞 Destek

- **Smithery.ai Documentation**: https://docs.smithery.ai
- **GitHub Issues**: Repository'de issue açın
- **Community**: Smithery Discord/Slack kanalları

## 🔄 Güncelleme

1. **Code değişiklikleri**
   - GitHub'a push edin
   - Smithery otomatik olarak yeniden deploy edecek

2. **Dependency güncellemeleri**
   - `requirements.txt` güncelleyin
   - `Dockerfile` gerekirse güncelleyin
   - Manuel redeploy yapın

3. **Environment variables**
   - Smithery dashboard'dan güncelleyin
   - Redeploy gerekli
