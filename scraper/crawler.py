import asyncio
import httpx
import json
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from config import BASE_URL, KEY_URLS, HEADERS, RAW_PAGES_DIR, MASTER_DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class ShardaCrawler:
    def __init__(self):
        self.visited = set()
        self.discovered_urls = set()
        self.assets_to_download = set()
        self.client = None

    async def init_client(self):
        self.client = httpx.AsyncClient(
            headers=HEADERS,
            timeout=30.0,
            follow_redirects=True,
            verify=False
        )

    async def fetch_page(self, item):
        url = item["url"]
        slug = item["slug"]
        category = item.get("category", "general")
        
        if url in self.visited:
            return None
        self.visited.add(url)

        try:
            logger.info(f"Fetching: {url} ({category})")
            resp = await self.client.get(url)
            if resp.status_code == 200:
                html = resp.text
                
                # Save raw HTML
                file_path = RAW_PAGES_DIR / f"{category}_{slug}.html"
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html)
                
                # Parse links & assets
                self.extract_links_and_assets(html, url)
                return {"url": url, "slug": slug, "category": category, "file_path": str(file_path), "status": 200}
            else:
                logger.warning(f"Failed to fetch {url}, status code: {resp.status_code}")
                return {"url": url, "slug": slug, "status": resp.status_code}
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return {"url": url, "slug": slug, "error": str(e)}

    def extract_links_and_assets(self, html, base_url):
        try:
            soup = BeautifulSoup(html, "html.parser")
            
            # Extract images and static media
            for img in soup.find_all(["img", "source", "link", "script"]):
                src = img.get("src") or img.get("data-src") or img.get("href")
                if src:
                    full_url = urljoin(base_url, src)
                    parsed = urlparse(full_url)
                    if any(ext in parsed.path.lower() for ext in [".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".ico", ".css", ".js"]):
                        self.assets_to_download.add(full_url)

            # Discover internal program and school links
            for a in soup.find_all("a", href=True):
                href = a["href"]
                full_url = urljoin(base_url, href)
                parsed = urlparse(full_url)
                if "sharda.ac.in" in parsed.netloc:
                    path = parsed.path.rstrip("/")
                    if any(prefix in path for prefix in ["/programmes/", "/course/", "/schools/", "/faculty/", "/admissions/"]):
                        if full_url not in self.visited and full_url not in self.discovered_urls:
                            self.discovered_urls.add(full_url)
        except Exception as e:
            logger.error(f"Error extracting links from {base_url}: {e}")

    async def crawl_all(self):
        await self.init_client()
        logger.info(f"Starting crawl for {len(KEY_URLS)} initial key routes...")
        
        tasks = [self.fetch_page(item) for item in KEY_URLS]
        results = await asyncio.gather(*tasks)
        
        logger.info(f"Initial crawl complete. Discovered {len(self.discovered_urls)} deep links and {len(self.assets_to_download)} asset URLs.")
        
        # Save crawl summary
        summary = {
            "total_pages_crawled": len(results),
            "discovered_links_count": len(self.discovered_urls),
            "discovered_links": list(self.discovered_urls)[:100],
            "assets_count": len(self.assets_to_download),
            "assets": list(self.assets_to_download)[:200]
        }
        
        with open(MASTER_DATA_DIR / "crawl_manifest.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
            
        with open(MASTER_DATA_DIR / "assets_manifest.json", "w", encoding="utf-8") as f:
            json.dump(list(self.assets_to_download), f, indent=2)

        await self.client.aclose()
        logger.info("Crawl manifest saved successfully.")

if __name__ == "__main__":
    crawler = ShardaCrawler()
    asyncio.run(crawler.crawl_all())
