import re
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(prefix="/search", tags=["Full-Text Search Engine"])

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_PATH = BASE_DIR / "backend" / "data" / "sharda_pages.db"

class SearchResultItem(BaseModel):
    slug: str
    title: str
    category: str
    snippet: str
    url: str
    score: float

class SearchResponse(BaseModel):
    query: str
    total_results: int
    category_filter: Optional[str]
    results: List[SearchResultItem]
    powered_by: str = "Turbo Bytes Consulting"

@router.get("", response_model=SearchResponse)
@router.get("/", response_model=SearchResponse)
def execute_full_text_search(
    q: str = Query(..., min_length=1, description="Search query keyword"),
    category: Optional[str] = Query(None, description="Optional category filter (programmes, schools, faculty, etc.)"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    if not DB_PATH.exists():
        return SearchResponse(query=q, total_results=0, category_filter=category, results=[])

    query_clean = q.strip().lower()
    query_terms = [t for t in re.findall(r'\w+', query_clean) if len(t) > 1]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    if category:
        cur.execute("SELECT slug, category, title, meta_description, content_text FROM pages WHERE category = ?", (category.lower(),))
    else:
        cur.execute("SELECT slug, category, title, meta_description, content_text FROM pages")
    
    rows = cur.fetchall()
    conn.close()

    scored_results = []
    for r in rows:
        slug, cat, title, meta_desc, text = r
        clean_slug = (slug or "").strip("/").lower()
        clean_title = title or clean_slug.replace("-", " ").title()
        content = text or meta_desc or ""

        score = 0
        title_lower = clean_title.lower()
        content_lower = content.lower()
        slug_lower = clean_slug.lower()

        # Exact phrase match bonus
        if query_clean in title_lower:
            score += 30
        if query_clean in slug_lower:
            score += 20
        if query_clean in content_lower:
            score += 10

        # Term matches
        for t in query_terms:
            if t in title_lower:
                score += 8
            if t in slug_lower:
                score += 5
            if t in content_lower:
                score += 2

        if score > 0:
            # Extract relevant highlighted snippet
            snippet = ""
            pos = content_lower.find(query_clean)
            if pos == -1 and query_terms:
                pos = content_lower.find(query_terms[0])
            
            if pos != -1:
                start = max(0, pos - 60)
                end = min(len(content), pos + 140)
                raw_snippet = content[start:end].strip()
                # Highlight query terms
                for t in query_terms:
                    raw_snippet = re.sub(rf"(?i)({re.escape(t)})", r"<strong>\1</strong>", raw_snippet)
                snippet = ("..." if start > 0 else "") + raw_snippet + ("..." if end < len(content) else "")
            else:
                snippet = (content[:150] + "...") if len(content) > 150 else content

            scored_results.append({
                "slug": clean_slug,
                "title": clean_title,
                "category": (cat or "general").upper(),
                "snippet": snippet or meta_desc or "Explore official Sharda University curriculum and admission guidelines.",
                "url": f"/{clean_slug}",
                "score": score
            })

    scored_results.sort(key=lambda x: x["score"], reverse=True)
    total_matches = len(scored_results)
    paginated = scored_results[offset:offset + limit]

    return SearchResponse(
        query=q,
        total_results=total_matches,
        category_filter=category,
        results=[SearchResultItem(**item) for item in paginated],
        powered_by="Turbo Bytes Consulting"
    )
