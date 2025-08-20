import asyncio
from mcp.server.fastmcp import FastMCP
from app import scrape_url, render_to_pptx, upload_to_github_release
import os
import logging

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("jama-abstract-generator")

@mcp.tool()
async def scrape_jama_article(url: str) -> dict:
    """
    JAMA Network makalesinden veri çeker ve yapılandırılmış formatta döndürür.
    """
    try:
        logger.info(f"Scraping JAMA article: {url}")
        # Run blocking function in executor
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
async def create_powerpoint(
    data: dict,
    output_filename: str = "visual_abstract.pptx",
    github_repo: str | None = None,
    github_token: str | None = None
) -> dict:
    """
    Çekilen makale verilerini kullanarak PowerPoint dosyası oluşturur.
    İsteğe bağlı olarak GitHub release'e yükler.
    """
    try:
        logger.info(f"Creating PowerPoint for: {data.get('title', 'Unknown title')}")
        loop = asyncio.get_event_loop()
        
        # Template ve output path ayarla
        template = os.environ.get("JAMA_TEMPLATE", "templates/abstract.pptx")
        out_dir = os.environ.get("OUTPUT_DIR", "outputs")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, output_filename)
        
        # PPTX oluştur
        await loop.run_in_executor(None, render_to_pptx, data, template, out_path)
        logger.info(f"PowerPoint created at: {out_path}")
        
        # GitHub'a yükle (opsiyonel)
        download_url = ""
        if github_repo and github_token:
            logger.info(f"Uploading to GitHub repo: {github_repo}")
            title = data.get("title", "JAMA Abstract")
            download_url, err = await loop.run_in_executor(
                None, upload_to_github_release, out_path, title, github_repo, github_token
            )
            if not download_url:
                logger.warning(f"GitHub upload failed: {err}")
                return {
                    "result": f"PPTX oluşturuldu, fakat GitHub yükleme başarısız: {err}",
                    "output_path": out_path,
                    "download_url": ""
                }
            logger.info(f"Successfully uploaded to GitHub: {download_url}")
        
        return {
            "result": "PPTX başarıyla oluşturuldu." + (" GitHub'a yüklendi." if download_url else ""),
            "output_path": out_path,
            "download_url": download_url or ""
        }
        
    except Exception as e:
        logger.error(f"Error creating PowerPoint: {str(e)}")
        return {
            "result": f"Hata: {str(e)}",
            "output_path": "",
            "download_url": ""
        }

if __name__ == "__main__":
    logger.info("Starting JAMA Abstract Generator MCP Server...")
    mcp.run()
