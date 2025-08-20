#!/usr/bin/env python3
"""
Vercel Deployment Script - Alternatif deployment yöntemi
"""

import json
import os
import subprocess
import sys
from pathlib import Path

def create_vercel_config():
    """Vercel konfigürasyon dosyası oluştur"""
    config = {
        "version": 2,
        "builds": [
            {
                "src": "server.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "/server.py"
            }
        ],
        "env": {
            "PYTHONPATH": ".",
            "PYTHONUNBUFFERED": "1",
            "JAMA_TEMPLATE": "templates/abstract.pptx",
            "OUTPUT_DIR": "outputs"
        }
    }
    
    with open("vercel.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ vercel.json oluşturuldu")

def create_requirements_vercel():
    """Vercel için requirements.txt güncelle"""
    requirements = [
        "fastmcp>=0.9.0",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.3",
        "lxml>=5.2.2",
        "python-pptx>=0.6.21",
        "aiofiles>=23.2.1"
    ]
    
    with open("requirements-vercel.txt", "w") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("✅ requirements-vercel.txt oluşturuldu")

def create_vercel_server():
    """Vercel için server dosyası oluştur"""
    server_code = '''
import asyncio
from mcp.server.fastmcp import FastMCP
from app import scrape_url, render_to_pptx, upload_to_github_release
import os
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simple HTTP health check server
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {
                "status": "healthy",
                "service": "jama-abstract-generator",
                "tools": ["scrape_jama_article", "create_powerpoint"]
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not Found")

def start_health_server():
    """Start HTTP health check server in a separate thread"""
    try:
        server = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 8000))), HealthCheckHandler)
        logger.info(f"Health check server started on port {os.environ.get('PORT', 8000)}")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Health server error: {e}")

# Create MCP server
mcp = FastMCP("jama-abstract-generator")

@mcp.tool()
async def scrape_jama_article(url: str) -> dict:
    """JAMA Network makalesinden veri çeker"""
    try:
        logger.info(f"Scraping JAMA article: {url}")
        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, scrape_url, url)
        
        logger.info(f"Successfully scraped data for: {data.get('title', 'Unknown title')}")
        return {
            "result": "Veri başarıyla çekildi.",
            "data": data
        }
    except Exception as e:
        logger.error(f"Error scraping article: {str(e)}")
        return {
            "result": f"Hata: {str(e)}",
            "data": None
        }

@mcp.tool()
async def create_powerpoint(data: dict, output_filename: str = "visual_abstract.pptx") -> dict:
    """PowerPoint dosyası oluşturur"""
    try:
        logger.info(f"Creating PowerPoint for: {data.get('title', 'Unknown title')}")
        loop = asyncio.get_event_loop()
        
        template = os.environ.get("JAMA_TEMPLATE", "templates/abstract.pptx")
        out_dir = os.environ.get("OUTPUT_DIR", "outputs")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, output_filename)
        
        await loop.run_in_executor(None, render_to_pptx, data, template, out_path)
        logger.info(f"PowerPoint created at: {out_path}")
        
        return {
            "result": "PPTX başarıyla oluşturuldu.",
            "output_path": out_path,
            "download_url": ""
        }
        
    except Exception as e:
        logger.error(f"Error creating PowerPoint: {str(e)}")
        return {
            "result": f"Hata: {str(e)}",
            "output_path": "",
            "download_url": ""
        }

if __name__ == "__main__":
    logger.info("Starting JAMA Abstract Generator MCP Server on Vercel...")
    
    # Start health check server in background thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Start MCP server
    mcp.run()
'''
    
    with open("server-vercel.py", "w", encoding="utf-8") as f:
        f.write(server_code)
    
    print("✅ server-vercel.py oluşturuldu")

def deploy_to_vercel():
    """Vercel'e deploy et"""
    print("🚀 Vercel'e deployment başlıyor...")
    
    # Vercel CLI kurulu mu kontrol et
    try:
        result = subprocess.run(["vercel", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Vercel CLI kurulu: {result.stdout.strip()}")
        else:
            print("❌ Vercel CLI kurulu değil")
            print("💡 Kurulum için: npm install -g vercel")
            return False
    except FileNotFoundError:
        print("❌ Vercel CLI bulunamadı")
        print("💡 Kurulum için: npm install -g vercel")
        return False
    
    # Deploy
    try:
        print("📦 Deploying to Vercel...")
        result = subprocess.run(["vercel", "--yes"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment başarılı!")
            print("🔗 URL:", result.stdout.strip())
            return True
        else:
            print("❌ Deployment hatası:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Deployment hatası: {e}")
        return False

def main():
    print("🚀 JAMA Abstract Generator - Vercel Deployment")
    print("=" * 50)
    
    # 1. Konfigürasyon dosyaları oluştur
    print("\n📋 Konfigürasyon dosyaları oluşturuluyor...")
    create_vercel_config()
    create_requirements_vercel()
    create_vercel_server()
    
    # 2. Deploy
    print("\n🚀 Deployment başlıyor...")
    success = deploy_to_vercel()
    
    if success:
        print("\n🎉 Deployment tamamlandı!")
        print("📋 Sonraki adımlar:")
        print("   1. Vercel dashboard'da projenizi kontrol edin")
        print("   2. MCP client'ınızda test edin")
        print("   3. Health check: /health endpoint")
    else:
        print("\n❌ Deployment başarısız!")
        print("💡 Manuel deployment için:")
        print("   1. https://vercel.com adresine gidin")
        print("   2. GitHub ile giriş yapın")
        print("   3. 'New Project' oluşturun")
        print("   4. Repository: aliemregencer/jama-abstract-mcp-v3")

if __name__ == "__main__":
    main()
