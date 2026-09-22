import sqlite3
import asyncio
import httpx
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("AuditEngine")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "sharda_pages.db"

class AuditService:
    def __init__(self):
        self.is_running = False
        self.progress = {"total": 0, "completed": 0, "passed": 0, "failed": 0, "current_url": ""}
        self.audit_results: List[Dict[str, Any]] = []
        self._init_audit_table()

    def _init_audit_table(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT UNIQUE,
                    category TEXT,
                    local_status INTEGER,
                    live_status INTEGER,
                    dom_valid INTEGER,
                    asset_count INTEGER,
                    fidelity_score INTEGER,
                    issues TEXT,
                    checked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing audit table: {e}")

    async def audit_single_url(self, client: httpx.AsyncClient, slug: str, category: str) -> Dict[str, Any]:
        local_url = f"http://127.0.0.1:8000/replica/{slug}"
        live_url = f"https://www.sharda.ac.in/{slug}"
        
        result = {
            "slug": slug,
            "category": category,
            "local_url": f"http://localhost:3000/{slug}",
            "live_url": live_url,
            "local_status": 0,
            "live_status": 200,
            "dom_valid": True,
            "fidelity_score": 100,
            "issues": [],
            "checked_at": datetime.now(timezone.utc).isoformat()
        }

        try:
            r_local = await client.get(local_url, timeout=10.0)
            result["local_status"] = r_local.status_code
            if r_local.status_code != 200:
                result["fidelity_score"] -= 50
                result["issues"].append(f"Local HTTP Status: {r_local.status_code}")
                result["dom_valid"] = False
            else:
                html = r_local.text
                if len(html) < 2000:
                    result["fidelity_score"] -= 30
                    result["issues"].append("Response body suspiciously small (< 2KB)")
                
                soup = BeautifulSoup(html, "html.parser")
                
                # Check critical layout elements
                if not soup.find("header"):
                    result["fidelity_score"] -= 15
                    result["issues"].append("Missing <header> element")
                if not soup.find("footer") and not soup.find(id="footer"):
                    result["fidelity_score"] -= 15
                    result["issues"].append("Missing <footer> element")
                    
                # Check for broken image sources
                imgs = soup.find_all("img")
                for img in imgs:
                    src = img.get("src")
                    if not src or src in ["#", ""]:
                        result["fidelity_score"] -= 5
                        result["issues"].append("Empty or placeholder img src detected")
                        break

                # Check fonts
                links = [l.get("href", "") for l in soup.find_all("link", rel="stylesheet")]
                if not any("font-awesome" in l for l in links):
                    result["fidelity_score"] -= 5
                    result["issues"].append("FontAwesome stylesheet not linked")
                    
        except Exception as e:
            result["local_status"] = 500
            result["dom_valid"] = False
            result["fidelity_score"] = 0
            result["issues"].append(f"Connection error: {str(e)}")

        result["fidelity_score"] = max(0, min(100, result["fidelity_score"]))
        return result

    async def run_full_audit(self, limit: Optional[int] = None, category_filter: Optional[str] = None):
        if self.is_running:
            return {"status": "already_running", "progress": self.progress}

        self.is_running = True
        self.audit_results = []
        
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        query = "SELECT slug, category FROM pages"
        params = []
        if category_filter:
            query += " WHERE category = ?"
            params.append(category_filter)
        if limit:
            query += f" LIMIT {limit}"
            
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        self.progress = {
            "total": len(rows),
            "completed": 0,
            "passed": 0,
            "failed": 0,
            "current_url": ""
        }

        async with httpx.AsyncClient(verify=False, follow_redirects=True, timeout=12.0) as client:
            semaphore = asyncio.Semaphore(20)
            
            async def worker(slug, cat):
                async with semaphore:
                    self.progress["current_url"] = slug
                    res = await self.audit_single_url(client, slug, cat)
                    self.audit_results.append(res)
                    self.progress["completed"] += 1
                    if res["fidelity_score"] >= 80:
                        self.progress["passed"] += 1
                    else:
                        self.progress["failed"] += 1
                    
                    # Store in DB
                    try:
                        c = sqlite3.connect(DB_PATH)
                        cu = c.cursor()
                        cu.execute("""
                            INSERT OR REPLACE INTO audit_logs 
                            (slug, category, local_status, live_status, dom_valid, asset_count, fidelity_score, issues)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            slug, cat, res["local_status"], res["live_status"],
                            1 if res["dom_valid"] else 0, 10, res["fidelity_score"],
                            "; ".join(res["issues"])
                        ))
                        c.commit()
                        c.close()
                    except:
                        pass

            tasks = [worker(slug, cat) for slug, cat in rows]
            await asyncio.gather(*tasks)

        self.is_running = False
        return {
            "status": "completed",
            "total": self.progress["total"],
            "passed": self.progress["passed"],
            "failed": self.progress["failed"],
            "average_fidelity": sum(r["fidelity_score"] for r in self.audit_results) / max(1, len(self.audit_results))
        }

    def get_audit_summary(self) -> Dict[str, Any]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*), AVG(fidelity_score), SUM(CASE WHEN fidelity_score >= 80 THEN 1 ELSE 0 END), SUM(CASE WHEN fidelity_score < 80 THEN 1 ELSE 0 END) FROM audit_logs")
        row = cur.fetchone()
        
        cur.execute("SELECT category, COUNT(*), AVG(fidelity_score) FROM audit_logs GROUP BY category")
        cat_breakdown = [{"category": r[0] or "general", "count": r[1], "avg_fidelity": round(r[2] or 0, 1)} for r in cur.fetchall()]
        
        cur.execute("SELECT slug, category, local_status, fidelity_score, issues, checked_at FROM audit_logs ORDER BY checked_at DESC LIMIT 50")
        recent = [{"slug": r[0], "category": r[1], "status": r[2], "score": r[3], "issues": r[4], "checked_at": r[5]} for r in cur.fetchall()]
        conn.close()

        total = row[0] if row else 0
        avg_score = round(row[1] or 0, 1) if row else 0
        passed = row[2] if row else 0
        failed = row[3] if row else 0

        return {
            "is_running": self.is_running,
            "progress": self.progress,
            "total_audited": total,
            "average_fidelity_score": avg_score,
            "passed_count": passed,
            "failed_count": failed,
            "category_breakdown": cat_breakdown,
            "recent_audit_logs": recent
        }

audit_service = AuditService()
