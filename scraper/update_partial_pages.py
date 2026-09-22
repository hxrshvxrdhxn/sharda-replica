import sqlite3
import httpx
import asyncio
from bs4 import BeautifulSoup
import json
import time

DB_PATH = 'backend/data/sharda_pages.db'
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

async def update_pages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, slug, url, length(content_html) FROM pages WHERE NOT (content_html LIKE '%<!DOCTYPE%' OR content_html LIKE '%<html%')")
    rows = cursor.fetchall()
    print(f"Found {len(rows)} pages to update to full HTML...")
    
    async with httpx.AsyncClient(headers=HEADERS, verify=False, timeout=15.0, follow_redirects=True) as client:
        for idx, (page_id, slug, url, current_len) in enumerate(rows):
            target_url = url if url.startswith("http") else f"https://www.sharda.ac.in/{slug.lstrip('/')}"
            try:
                resp = await client.get(target_url)
                if resp.status_code == 200 and len(resp.text) > 5000:
                    soup = BeautifulSoup(resp.text, "html.parser")
                    title = soup.title.string.strip() if soup.title and soup.title.string else f"{slug.replace('-', ' ').title()} - Sharda University"
                    meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                    meta_desc = meta_tag.get("content", "").strip() if meta_tag else ""
                    
                    cursor.execute("""
                        UPDATE pages 
                        SET title = ?, meta_description = ?, content_html = ?, status_code = 200
                        WHERE id = ?
                    """, (title, meta_desc, resp.text, page_id))
                    conn.commit()
                    print(f"[{idx+1}/{len(rows)}] Updated: {slug} (Len: {len(resp.text)})")
                else:
                    print(f"[{idx+1}/{len(rows)}] Skip/Failed: {slug} (Status: {resp.status_code})")
            except Exception as e:
                print(f"[{idx+1}/{len(rows)}] Error {slug}: {e}")
            await asyncio.sleep(0.1)

    # Re-count
    cursor.execute("SELECT count(*) FROM pages WHERE content_html LIKE '%<!DOCTYPE%' OR content_html LIKE '%<html%'")
    full_count = cursor.fetchone()[0]
    cursor.execute("SELECT count(*) FROM pages")
    total_count = cursor.fetchone()[0]
    print(f"\nCompleted! Full HTML documents now: {full_count} / {total_count} pages.")
    conn.close()

if __name__ == '__main__':
    asyncio.run(update_pages())
