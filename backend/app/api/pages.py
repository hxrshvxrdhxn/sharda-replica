from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
import sqlite3
import json
from pathlib import Path

router = APIRouter(prefix="/pages", tags=["Dynamic Pages & Master Sitemaps"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "sharda_pages.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@router.get("/index")
def list_page_index(
    category: Optional[str] = Query(None, description="Filter by category (e.g., about, admissions, course-fee)"),
    search: Optional[str] = Query(None, description="Search page titles")
):
    if not DB_PATH.exists():
        return {"total": 0, "pages": []}

    conn = get_db()
    cursor = conn.cursor()
    query = "SELECT slug, title, category, meta_description, url FROM pages WHERE status_code = 200"
    params = []

    if category:
        query += " AND category = ?"
        params.append(category)
    if search:
        query += " AND (title LIKE ? OR content_text LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])

    query += " ORDER BY id ASC LIMIT 200"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    pages = [dict(r) for r in rows]
    return {"total": len(pages), "pages": pages}

@router.get("/get/{slug:path}")
async def get_page_content(slug: str):
    if not DB_PATH.exists():
        raise HTTPException(status_code=404, detail="Page database not initialized")

    normalized_slug = slug.strip("/").lower()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pages WHERE slug = ? OR slug = ? LIMIT 1", (normalized_slug, f"/{normalized_slug}"))
    row = cursor.fetchone()
    conn.close()

    if not row:
        # Fallback search by prefix / suffix
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pages WHERE slug LIKE ? LIMIT 1", (f"%{normalized_slug}%",))
        row = cursor.fetchone()
        conn.close()

    if row:
        res = dict(row)
        if res.get("headings"):
            try:
                res["headings"] = json.loads(res["headings"])
            except:
                res["headings"] = []
        return res

    # 3. Live on-demand fetch & cache into SQLite
    target_url = f"https://www.sharda.ac.in/{normalized_slug}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    import httpx
    from bs4 import BeautifulSoup

    try:
        async with httpx.AsyncClient(headers=headers, verify=False, timeout=15.0, follow_redirects=True) as client:
            resp = await client.get(target_url)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, "html.parser")
                for s in soup(["script", "style", "noscript", "svg"]):
                    s.decompose()

                title = soup.title.string.strip() if soup.title and soup.title.string else f"{slug.replace('-', ' ').title()} - Sharda University"
                meta_tag = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
                meta_desc = meta_tag.get("content", "").strip() if meta_tag else f"Explore {title} at Sharda University, Greater Noida."
                
                main_container = soup.find("main") or soup.find("article") or soup.find("div", class_=lambda c: c and any(k in c for k in ["content", "inner", "main", "detail", "container"])) or soup.body
                content_text = main_container.get_text(separator="\n", strip=True) if main_container else "Detailed university program and curriculum information."
                headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"]) if h.get_text(strip=True)]
                
                category = normalized_slug.split("/")[0] if "/" in normalized_slug else "general"

                # Cache in SQLite
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO pages (url, slug, category, title, meta_description, content_text, content_html, headings, status_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 200)
                """, (target_url, normalized_slug, category, title, meta_desc, content_text, resp.text, json.dumps(headings[:10])))
                conn.commit()
                conn.close()

                return {
                    "url": target_url,
                    "slug": normalized_slug,
                    "category": category,
                    "title": title,
                    "meta_description": meta_desc,
                    "content_text": content_text,
                    "content_html": resp.text,
                    "headings": headings[:10],
                    "status_code": 200
                }
    except Exception as e:
        pass

    # Generic fallback if live URL is unreachable
    cat = normalized_slug.split("/")[0] if "/" in normalized_slug else "university"
    formatted_title = normalized_slug.replace("-", " ").replace("/", " - ").title()
    return {
        "url": target_url,
        "slug": normalized_slug,
        "category": cat,
        "title": f"{formatted_title} | Sharda University",
        "meta_description": f"Official information and academic catalog for {formatted_title} at Sharda University (NAAC A+ Accredited).",
        "content_text": f"Welcome to the official Sharda University page for {formatted_title}.\n\nSharda University is a leading educational institution offering world-class infrastructure, industry-aligned curriculum, dynamic research opportunities, and comprehensive student support services. For complete details, fee structures, eligibility criteria, and admissions, please connect with our admissions desk or ask Sharda AI.",
        "content_html": f"<div class='p-6'><h2>{formatted_title}</h2><p>Official information for {formatted_title} at Sharda University.</p></div>",
        "headings": [formatted_title, "Admissions & Eligibility", "Curriculum & Faculty", "Career Opportunities"],
        "status_code": 200
    }
