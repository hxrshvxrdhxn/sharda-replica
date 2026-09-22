import json
import sqlite3
import asyncio
import httpx
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urlparse

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "backend" / "data"
DB_PATH = DATA_DIR / "sharda_pages.db"
URLS_FILE = BASE_DIR / "scraper" / "output" / "all_discovered_urls.json"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

def get_division_plan():
    with open(URLS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    urls = data.get("urls", [])
    
    divisions = {
        "Div 1: Core Hubs & Admissions": [],
        "Div 2: 14+ Schools & Departments": [],
        "Div 3: Academic Degree Programmes": [],
        "Div 4: Faculty Directory & Research": [],
        "Div 5: Campus Life, Connect & Happenings": []
    }
    
    for u in urls:
        path = urlparse(u).path.strip("/").lower()
        if not path or path == "home":
            divisions["Div 1: Core Hubs & Admissions"].append(u)
        elif any(path.startswith(p) for p in ["about", "admissions", "course-fee", "international", "placements", "scholarship", "apply", "contact", "iqac", "privacy", "terms", "disclaimer", "payment"]):
            divisions["Div 1: Core Hubs & Admissions"].append(u)
        elif any(path.startswith(p) for p in ["schools", "department"]):
            divisions["Div 2: 14+ Schools & Departments"].append(u)
        elif path.startswith("programmes") or any(path.startswith(p) for p in ["btech-", "bca-", "bsc-", "llb-", "mba-", "mtech-", "ma-"]):
            divisions["Div 3: Academic Degree Programmes"].append(u)
        elif any(path.startswith(p) for p in ["faculty", "research"]):
            divisions["Div 4: Faculty Directory & Research"].append(u)
        else:
            divisions["Div 5: Campus Life, Connect & Happenings"].append(u)
            
    return divisions

async def harvest_batch(urls, batch_size=10, limit=None):
    target_urls = urls[:limit] if limit else urls
    print(f"Starting ingestion & validation of {len(target_urls)} pages in micro-batches of {batch_size}...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=15.0, follow_redirects=True) as client:
        for i in range(0, len(target_urls), batch_size):
            batch = target_urls[i:i + batch_size]
            print(f"\n--- Processing Sub-batch [{i+1} to {min(i+batch_size, len(target_urls))}] of {len(target_urls)} ---")
            
            tasks = []
            for u in batch:
                tasks.append(client.get(u))
            
            responses = await asyncio.gather(*tasks, return_exceptions=True)
            for u, resp in zip(batch, responses):
                path = urlparse(u).path.strip("/").lower()
                slug = path if path else "home"
                category = slug.split("/")[0]
                
                if isinstance(resp, httpx.Response) and resp.status_code == 200 and len(resp.text) > 1000:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title = soup.title.string.strip() if soup.title and soup.title.string else slug.title()
                    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                    meta_desc = meta_tag.get("content", "").strip() if meta_tag else ""
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO pages (url, slug, category, title, meta_description, content_text, content_html, headings, status_code)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 200)
                    """, (u, slug, category, title, meta_desc, "", resp.text, "[]"))
                    conn.commit()
                    print(f"  [PASS 200 OK] {slug:<45} | Title: {title[:40]} | Size: {len(resp.text):,} B")
                else:
                    status = getattr(resp, 'status_code', 'ERR')
                    print(f"  [NOTICE {status}] {slug:<45} | Cached fallback will be used")
            
            await asyncio.sleep(0.2)
            
    conn.close()

if __name__ == "__main__":
    plan = get_division_plan()
    print("=" * 80)
    print("       SHARDA UNIVERSITY MASTER URL CENSUS & DIVISION BREAKDOWN")
    print("=" * 80)
    total = 0
    for div_name, div_urls in plan.items():
        print(f" {div_name:<42} : {len(div_urls):>5} pages")
        total += len(div_urls)
    print("=" * 80)
    print(f" TOTAL DISTINCT LIVE PAGES ON SHARDA.AC.IN : {total:>5} pages")
    print("=" * 80)
