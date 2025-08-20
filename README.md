# JAMA Abstract Generator MCP Server

JAMA Network makale URL'lerinden görsel özet içeren PowerPoint dosyaları oluşturan MCP (Model Context Protocol) server.

## 🚀 Features

- **JAMA Article Scraping**: JAMA Network makalelerinden otomatik veri çekme
- **PowerPoint Generation**: Çekilen verileri kullanarak görsel özet PPTX dosyası oluşturma
- **GitHub Integration**: Opsiyonel olarak GitHub release'e otomatik yükleme
- **MCP Protocol**: Fast-MCP ile modern MCP server implementasyonu
- **Smithery Ready**: Cloud deployment için optimize edilmiş

## 🛠️ Installation

### Local Development

```bash
# Clone repository
git clone <repository-url>
cd scrape-to-pptx

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m server
```

### Smithery Deployment

```bash
# Install Smithery CLI
npm install -g @smithery/cli

# Login to Smithery
smithery auth login

# Deploy to Smithery
./deploy.sh
```

## 📋 Requirements

- Python 3.11+
- Fast-MCP >= 0.9.0
- BeautifulSoup4 >= 4.12.3
- python-pptx >= 0.6.21
- requests >= 2.31.0

## 🔧 Configuration

### Environment Variables

- `JAMA_TEMPLATE`: PowerPoint template dosyası yolu (varsayılan: `templates/abstract.pptx`)
- `OUTPUT_DIR`: Çıktı dosyaları için dizin (varsayılan: `outputs`)
- `PYTHONPATH`: Python path ayarı (varsayılan: `.`)

### MCP Tools

#### 1. `scrape_jama_article`

JAMA Network makalesinden veri çeker.

**Input:**
```json
{
  "url": "https://jamanetwork.com/journals/jama/fullarticle/..."
}
```

**Output:**
```json
{
  "result": "Veri başarıyla çekildi.",
  "data": {
    "url": "...",
    "title": "...",
    "va": {
      "the_study": {
        "participants": "...",
        "intervention": "...",
        "comparator": "...",
        "primary_outcome": "...",
        "settings_locations": "..."
      },
      "findings": {
        "summary": "...",
        "key_numbers": []
      }
    }
  }
}
```

#### 2. `create_powerpoint`

Çekilen verileri kullanarak PowerPoint dosyası oluşturur.

**Input:**
```json
{
  "data": { /* scrape_jama_article output */ },
  "output_filename": "visual_abstract.pptx",
  "github_repo": "username/repo",
  "github_token": "ghp_..."
}
```

**Output:**
```json
{
  "result": "PPTX başarıyla oluşturuldu.",
  "output_path": "/path/to/output.pptx",
  "download_url": "https://github.com/..."
}
```

## 🐳 Docker

```bash
# Build image
docker build -t jama-abstract-generator .

# Run container
docker run -p 8000:8000 jama-abstract-generator
```

## ☁️ Smithery Deployment

### Prerequisites

1. Smithery CLI kurulu olmalı
2. Smithery hesabında giriş yapılmış olmalı
3. Proje oluşturulmuş olmalı

### Deployment Steps

1. **Konfigürasyon Kontrolü**
   ```bash
   # smithery.yaml dosyasını kontrol et
   cat smithery.yaml
   ```

2. **Deploy Et**
   ```bash
   ./deploy.sh
   ```

3. **Status Kontrolü**
   ```bash
   smithery status
   smithery logs
   ```

### Smithery Konfigürasyonu

`smithery.yaml` dosyası şu ayarları içerir:

- **Build**: Dockerfile tabanlı build
- **Runtime**: Environment variables ve resource limits
- **Health Check**: `/health` endpoint ile sağlık kontrolü
- **Scaling**: Otomatik ölçeklendirme (1-3 replica)
- **Volumes**: Kalıcı depolama için volume mount'lar

## 🔍 Health Check

Server sağlık durumu `/health` endpoint'inden kontrol edilebilir:

```bash
curl https://your-smithery-url/health
```

Response:
```json
{
  "status": "healthy",
  "service": "jama-abstract-generator"
}
```

## 📁 Project Structure

```
scrape-to-pptx/
├── app.py                 # Ana uygulama mantığı
├── server.py             # Fast-MCP server
├── mcp.yaml             # MCP konfigürasyonu
├── smithery.yaml        # Smithery deployment konfigürasyonu
├── Dockerfile           # Docker image tanımı
├── deploy.sh            # Deployment script'i
├── requirements.txt     # Python dependencies
├── templates/           # PowerPoint template'leri
├── outputs/             # Oluşturulan dosyalar
└── icons/               # UI icon'ları
```

## 🚨 Troubleshooting

### Common Issues

1. **Template Not Found**
   - `templates/abstract.pptx` dosyasının var olduğundan emin olun
   - `JAMA_TEMPLATE` environment variable'ını kontrol edin

2. **Permission Errors**
   - `outputs/` dizininin yazılabilir olduğundan emin olun
   - Docker container'da volume mount'ları kontrol edin

3. **Smithery Deployment Failures**
   - `smithery auth status` ile giriş durumunu kontrol edin
   - Resource limits'i kontrol edin (CPU, memory, storage)

### Logs

```bash
# Local logs
python -m server

# Smithery logs
smithery logs

# Docker logs
docker logs <container-id>
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Fast-MCP team for the excellent MCP server framework
- Smithery team for cloud deployment platform
- JAMA Network for providing medical research articles
