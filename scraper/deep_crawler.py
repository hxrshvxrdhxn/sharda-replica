import asyncio
import httpx
import re
import json
import sqlite3
import logging
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("DeepCrawler")

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
DB_PATH = DATA_DIR / "sharda_pages.db"
DATA_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE,
            slug TEXT UNIQUE,
            category TEXT,
            title TEXT,
            meta_description TEXT,
            headings TEXT,
            content_text TEXT,
            content_html TEXT,
            status_code INTEGER,
            last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_slug ON pages (slug)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_category ON pages (category)")
    conn.commit()
    conn.close()

async def get_all_sitemap_urls():
    logger.info("Fetching complete master sitemap from https://www.sharda.ac.in/sitemap.xml...")
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=30.0) as client:
        resp = await client.get("https://www.sharda.ac.in/sitemap.xml")
        if resp.status_code == 200:
            urls = re.findall(r'<loc>(.*?)</loc>', resp.text)
            logger.info(f"Discovered {len(urls)} URLs in official sitemap.xml")
            return list(set(urls))
    return []

def clean_html(html_str):
    soup = BeautifulSoup(html_str, "html.parser")
    for tag in soup(["script", "style", "noscript", "iframe", "svg"]):
        tag.decompose()
    return soup

async def fetch_and_save(client, url, semaphore):
    async with semaphore:
        parsed = urlparse(url)
        slug = parsed.path.strip("/").lower()
        if not slug:
            slug = "home"
        
        parts = slug.split("/")
        category = parts[0] if parts else "general"

        try:
            resp = await client.get(url, timeout=15.0, follow_redirects=True)
            if resp.status_code == 200:
                soup = clean_html(resp.text)
                
                title = soup.title.text.strip() if soup.title else slug.replace("-", " ").title()
                meta_desc = ""
                meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                if meta_tag:
                    meta_desc = meta_tag.get("content", "").strip()

                # Extract headings
                headings = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"]) if h.text.strip()]

                # Extract main body text
                main_tag = soup.find("main") or soup.find("div", id="content") or soup.find("div", class_="content") or soup.find("body")
                content_text = ""
                content_html = ""
                if main_tag:
                    content_text = re.sub(r'\s+', ' ', main_tag.get_text()).strip()
                    content_html = str(main_tag)
                else:
                    content_text = re.sub(r'\s+', ' ', soup.get_text()).strip()
                    content_html = str(soup)

                # Save to database
                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO pages 
                    (url, slug, category, title, meta_description, headings, content_text, content_html, status_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (url, slug, category, title, meta_desc, json.dumps(headings), content_text[:15000], content_html[:50000], 200))
                conn.commit()
                conn.close()

                return {"slug": slug, "title": title, "category": category, "status": 200}
        except Exception as e:
            return {"slug": slug, "url": url, "error": str(e), "status": 500}

async def run_deep_harvest(batch_size: int = 150):
    init_db()
    urls = await get_all_sitemap_urls()
    if not urls:
        logger.error("No URLs found in sitemap.")
        return

    logger.info(f"Targeting {min(len(urls), batch_size)} priority URLs across schools, departments, fees, admissions, research, and campus life...")
    
    # Prioritize key categories
    prioritized_urls = []
    other_urls = []
    for u in urls:
        if any(k in u for k in ["/about", "/admissions", "/course", "/programme", "/scholarship", "/schools", "/placements", "/campus", "/research", "/international", "/contact", "/fee"]):
            prioritized_urls.append(u)
        else:
            other_urls.append(u)
            
    all_target_urls = (prioritized_urls + other_urls)[:batch_size]
    
    semaphore = asyncio.Semaphore(25)
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=20.0) as client:
        tasks = [fetch_and_save(client, url, semaphore) for url in all_target_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    successful = [r for r in results if isinstance(r, dict) and r.get("status") == 200]
    logger.info(f"Deep crawl completed: {len(successful)} pages ingested and stored into {DB_PATH}")

    # Export index for fast lookup
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT slug, title, category, meta_description FROM pages WHERE status_code = 200")
    rows = cursor.fetchall()
    conn.close()

    index = [{"slug": r[0], "title": r[1], "category": r[2], "description": r[3]} for r in rows]
    with open(DATA_DIR / "pages_index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    logger.info(f"Generated master page index with {len(index)} searchable page routes.")

if __name__ == "__main__":
    asyncio.run(run_deep_harvest(batch_size=200))
