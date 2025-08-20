# 🚀 Hızlı Deployment Rehberi

## ✅ Proje Hazır!

JAMA Abstract Generator MCP Server Smithery.ai'de deployment yapılmaya hazır!

## 🎯 Deployment Adımları:

### 1. Smithery.ai Web Interface (Önerilen)

1. **Smithery.ai'ye gidin**: https://smithery.ai
2. **GitHub ile giriş yapın**
3. **"New Project" butonuna tıklayın**
4. **Proje bilgilerini girin**:
   - **Name**: `jama-abstract-generator`
   - **Description**: `JAMA Network makale URL'sinden görsel özet içeren PowerPoint dosyası oluşturan MCP server`
   - **Repository**: `aliemregencer/jama-abstract-mcp-v3`
   - **Branch**: `main`
5. **"Create Project" butonuna tıklayın**
6. **"Deploy" butonuna tıklayın**
7. **Build tamamlanana kadar bekleyin**

### 2. Environment Variables (Opsiyonel)

```
PYTHONPATH=/app
PYTHONUNBUFFERED=1
JAMA_TEMPLATE=templates/abstract.pptx
OUTPUT_DIR=outputs
```

### 3. Deployment Sonrası

- ✅ MCP server çalışıyor
- ✅ Health check endpoint: `/health`
- ✅ 2 MCP tool hazır:
  - `scrape_jama_article`
  - `create_powerpoint`

## 🔧 MCP Client Konfigürasyonu:

```yaml
# MCP client config
- name: jama-abstract-generator
  transport: smithery
  config:
    project: jama-abstract-generator
    api_key: YOUR_SMITHERY_API_KEY
```

## 📊 Test Etme:

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

## 🚨 Sorun Giderme:

- **Build hatası**: Dockerfile syntax kontrolü
- **Runtime hatası**: Environment variables kontrolü
- **MCP hatası**: Server logları kontrolü

## 📞 Destek:

- **Smithery.ai**: https://smithery.ai
- **GitHub Issues**: Repository'de issue açın
- **Documentation**: `deployment-guide.md` dosyasını okuyun

---

**🎉 Deployment tamamlandıktan sonra MCP server'ınız kullanıma hazır olacak!**
