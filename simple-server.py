#!/usr/bin/env python3
"""
Basit HTTP Server - Health Check ve Test için
"""

import http.server
import socketserver
import json
import logging
from pathlib import Path

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>JAMA Abstract Generator</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; }
                    .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
                    .success { background-color: #d4edda; color: #155724; }
                    .info { background-color: #d1ecf1; color: #0c5460; }
                </style>
            </head>
            <body>
                <h1>🚀 JAMA Abstract Generator MCP Server</h1>
                
                <div class="status success">
                    <h3>✅ Server Çalışıyor!</h3>
                    <p>Bu server Smithery.ai'de deployment yapılmaya hazır.</p>
                </div>
                
                <div class="status info">
                    <h3>📋 MCP Tools:</h3>
                    <ul>
                        <li><strong>scrape_jama_article</strong> - JAMA makalelerinden veri çeker</li>
                        <li><strong>create_powerpoint</strong> - PowerPoint dosyası oluşturur</li>
                    </ul>
                </div>
                
                <div class="status info">
                    <h3>🔗 Endpoints:</h3>
                    <ul>
                        <li><a href="/health">/health</a> - Health check</li>
                        <li><a href="/status">/status</a> - Server durumu</li>
                        <li><a href="/tools">/tools</a> - MCP tools listesi</li>
                    </ul>
                </div>
                
                <div class="status info">
                    <h3>🚀 Deployment:</h3>
                    <p>Smithery.ai'de deployment yapmak için:</p>
                    <ol>
                        <li><a href="https://smithery.ai" target="_blank">https://smithery.ai</a> adresine gidin</li>
                        <li>GitHub ile giriş yapın</li>
                        <li>Repository: <code>aliemregencer/jama-abstract-mcp-v3</code></li>
                        <li>Branch: <code>main</code></li>
                    </ol>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "status": "healthy",
                "service": "jama-abstract-generator",
                "version": "1.0.0",
                "tools": ["scrape_jama_article", "create_powerpoint"]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            # Check if required files exist
            files_status = {
                "server.py": Path("server.py").exists(),
                "app.py": Path("app.py").exists(),
                "requirements.txt": Path("requirements.txt").exists(),
                "Dockerfile": Path("Dockerfile").exists(),
                "templates/": Path("templates").exists(),
                "outputs/": Path("outputs").exists()
            }
            
            response = {
                "status": "ready",
                "service": "jama-abstract-generator",
                "files": files_status,
                "deployment_ready": all(files_status.values())
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        elif self.path == '/tools':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "tools": [
                    {
                        "name": "scrape_jama_article",
                        "description": "JAMA Network makalesinden veri çeker",
                        "input": {"url": "string"},
                        "output": {"result": "string", "data": "object"}
                    },
                    {
                        "name": "create_powerpoint",
                        "description": "PowerPoint dosyası oluşturur",
                        "input": {"data": "object", "output_filename": "string"},
                        "output": {"result": "string", "output_path": "string"}
                    }
                ]
            }
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")
    
    def log_message(self, format, *args):
        logger.info(f"{self.client_address[0]} - {format % args}")

def main():
    PORT = 8000
    
    try:
        with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
            logger.info(f"🚀 Server başlatıldı - http://localhost:{PORT}")
            logger.info(f"📋 Health check: http://localhost:{PORT}/health")
            logger.info(f"🔍 Server durumu: http://localhost:{PORT}/status")
            logger.info(f"🛠️  MCP Tools: http://localhost:{PORT}/tools")
            logger.info(f"🌐 Ana sayfa: http://localhost:{PORT}/")
            logger.info("⏹️  Durdurmak için Ctrl+C")
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        logger.info("🛑 Server durduruldu")
    except Exception as e:
        logger.error(f"❌ Server hatası: {e}")

if __name__ == "__main__":
    main()
