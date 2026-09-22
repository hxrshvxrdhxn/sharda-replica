import asyncio
import httpx
import re
import json
import sqlite3
import logging
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("FullHarvester")

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
            tier INTEGER,
            title TEXT,
            meta_description TEXT,
            headings TEXT,
            content_text TEXT,
            content_html TEXT,
            status_code INTEGER,
            last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Check if tier column exists
    cursor.execute("PRAGMA table_info(pages)")
    cols = [row[1] for row in cursor.fetchall()]
    if "tier" not in cols:
        cursor.execute("ALTER TABLE pages ADD COLUMN tier INTEGER")
    if "headings" not in cols:
        cursor.execute("ALTER TABLE pages ADD COLUMN headings TEXT")

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_slug ON pages (slug)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_tier ON pages (tier)")
    conn.commit()
    conn.close()

def assign_tier(slug: str) -> int:
    if slug == "home" or slug == "":
        return 0
    if any(slug.startswith(p) for p in ["about", "admissions", "course-fee", "international", "placements", "scholarship"]):
        return 1
    if any(slug.startswith(p) for p in ["schools", "department"]):
        return 2
    if slug.startswith("programmes"):
        return 3
    if any(slug.startswith(p) for p in ["faculty", "research"]):
        return 4
    return 5

async def fetch_page(client, url, semaphore):
    async with semaphore:
        parsed = urlparse(url)
        slug = parsed.path.strip("/").lower()
        if not slug:
            slug = "home"
        
        category = slug.split("/")[0] if slug else "general"
        tier = assign_tier(slug)

        try:
            resp = await client.get(url, timeout=18.0, follow_redirects=True)
            if resp.status_code == 200:
                html = resp.text
                soup = BeautifulSoup(html, "html.parser")
                
                title = soup.title.text.strip() if soup.title else slug.replace("-", " ").title()
                meta_desc = ""
                m = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                if m:
                    meta_desc = m.get("content", "").strip()

                # Extract main text
                for tag in soup(["script", "style", "noscript", "svg", "iframe"]):
                    tag.decompose()
                
                text = re.sub(r'\s+', ' ', soup.get_text()).strip()

                conn = sqlite3.connect(DB_PATH)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO pages 
                    (url, slug, category, tier, title, meta_description, headings, content_text, content_html, status_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (url, slug, category, tier, title, meta_desc, "[]", text[:15000], html[:60000], 200))
                conn.commit()
                conn.close()

                return {"slug": slug, "tier": tier, "status": 200}
        except Exception as e:
            return {"slug": slug, "error": str(e), "status": 500}

async def harvest_all(max_pages: int = 500):
    init_db()
    urls_file = BASE_DIR / "scraper" / "output" / "all_discovered_urls.json"
    if not urls_file.exists():
        logger.error("all_discovered_urls.json not found.")
        return

    with open(urls_file, "r") as f:
        data = json.load(f)
    urls = data["urls"]

    # Sort URLs to ensure Tier 0, 1, 2, 3 are prioritized
    def priority_sort(u):
        if "/programmes" in u: return 1
        if "/schools" in u: return 2
        if "/admissions" in u: return 3
        if "/about" in u: return 4
        if "/faculty" in u: return 5
        return 6

    sorted_urls = sorted(urls, key=priority_sort)[:max_pages]
    logger.info(f"Starting parallel ingestion for {len(sorted_urls)} priority tier URLs (40 workers)...")

    semaphore = asyncio.Semaphore(35)
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=25.0) as client:
        tasks = [fetch_page(client, url, semaphore) for url in sorted_urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    success_count = sum(1 for r in results if isinstance(r, dict) and r.get("status") == 200)
    logger.info(f"Ingestion completed: {success_count} pages stored into {DB_PATH}")

if __name__ == "__main__":
    asyncio.run(harvest_all(max_pages=500))
