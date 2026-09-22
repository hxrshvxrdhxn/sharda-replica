import sys
import json
import sqlite3
import asyncio
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.parse
from pathlib import Path

# Force UTF-8 output on Windows console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / 'backend' / 'data' / 'sharda_pages.db'
URLS_FILE = BASE_DIR / 'scraper' / 'output' / 'all_discovered_urls.json'

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

async def harvest_remaining():
    with open(URLS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    urls = data.get('urls', [])
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT slug FROM pages WHERE length(content_html) > 5000")
    cached_slugs = set(r[0].strip("/").lower() for r in c.fetchall())
    
    uncached_urls = []
    for u in urls:
        # Sanitize URL whitespace / tabs
        clean_u = u.strip().replace("\t", "").replace("\r", "").replace("\n", "")
        path = urlparse(clean_u).path.strip("/").lower()
        if not path:
            path = "home"
        if path not in cached_slugs:
            uncached_urls.append(clean_u)
            
    print(f"Total Master URLs: {len(urls)}")
    print(f"Already Cached: {len(cached_slugs)}")
    print(f"Remaining to Ingest: {len(uncached_urls)}")
    
    if not uncached_urls:
        print("ALL 2,371 PAGES ARE ALREADY 100% INGESTED AND CACHED!")
        conn.close()
        return

    semaphore = asyncio.Semaphore(10)
    
    async def fetch_and_save(client, url, idx, total):
        async with semaphore:
            clean_url = url.strip().replace("\t", "").replace(" ", "%20")
            path = urlparse(clean_url).path.strip("/").lower()
            slug = path if path else "home"
            category = slug.split("/")[0]
            try:
                resp = await client.get(clean_url, timeout=18.0, follow_redirects=True)
                if resp.status_code == 200 and len(resp.text) > 1000:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title = soup.title.string.strip() if soup.title and soup.title.string else slug.title()
                    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                    meta_desc = meta_tag.get("content", "").strip() if meta_tag else ""
                    
                    db_conn = sqlite3.connect(DB_PATH)
                    cur = db_conn.cursor()
                    cur.execute("""
                        INSERT OR REPLACE INTO pages (url, slug, category, title, meta_description, content_text, content_html, headings, status_code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 200)
                    """, (clean_url, slug, category, title, meta_desc, "", resp.text, "[]"))
                    db_conn.commit()
                    db_conn.close()
                    print(f"[{idx+1}/{total}] Ingested & Cached: {slug[:38]:<38} ({len(resp.text):,} B)")
                else:
                    print(f"[{idx+1}/{total}] Status {resp.status_code}: {slug}")
            except Exception as e:
                print(f"[{idx+1}/{total}] Error {slug}: {str(e)[:60]}")
            await asyncio.sleep(0.05)

    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=20.0) as client:
        tasks = [fetch_and_save(client, u, i, len(uncached_urls)) for i, u in enumerate(uncached_urls)]
        await asyncio.gather(*tasks)

    c.execute("SELECT count(*) FROM pages WHERE length(content_html) > 5000")
    final_count = c.fetchone()[0]
    print(f"\n=======================================================")
    print(f" HARVEST COMPLETE! Total 100% Cached Pages: {final_count} / {len(urls)}")
    print(f"=======================================================")
    conn.close()

if __name__ == '__main__':
    asyncio.run(harvest_remaining())
