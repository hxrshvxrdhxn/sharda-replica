import sqlite3
import logging
import httpx
import csv
import io
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pathlib import Path
from ..core.config import settings

logger = logging.getLogger("CRMService")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "sharda_pages.db"

class CRMLeadService:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lead_id TEXT UNIQUE,
                    full_name TEXT,
                    email TEXT,
                    phone TEXT,
                    city TEXT,
                    state TEXT,
                    interested_school TEXT,
                    interested_course TEXT,
                    lead_source TEXT,
                    lead_intent_score INTEGER,
                    lead_priority TEXT,
                    status TEXT DEFAULT 'NEW',
                    notes TEXT DEFAULT '',
                    utm_source TEXT DEFAULT 'organic',
                    utm_medium TEXT DEFAULT 'direct',
                    utm_campaign TEXT DEFAULT 'sharda_rebuild_2026',
                    chat_transcript TEXT DEFAULT '',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing leads table: {e}")

    @staticmethod
    def calculate_lead_score(lead_data: Dict[str, Any]) -> int:
        score = 25  # Baseline for form initiation
        if lead_data.get("phone"):
            score += 30
        if lead_data.get("email"):
            score += 20
        if lead_data.get("interested_course"):
            score += 15
        if lead_data.get("source") in ["ai_assistant", "fee_calculator", "scholarship_checker", "suat_portal"]:
            score += 10
        return min(score, 100)

    def save_lead(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        score = self.calculate_lead_score(lead_data)
        priority = "HOT" if score >= 75 else "WARM" if score >= 50 else "COLD"
        lead_id = f"SU-{int(datetime.now(timezone.utc).timestamp())}-{abs(hash(lead_data.get('email', '') + lead_data.get('phone', ''))) % 10000:04d}"

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO leads (
                lead_id, full_name, email, phone, city, state, 
                interested_school, interested_course, lead_source, 
                lead_intent_score, lead_priority, status, notes,
                utm_source, utm_medium, utm_campaign, chat_transcript
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            lead_id,
            lead_data.get("full_name", "Prospective Student"),
            lead_data.get("email", ""),
            lead_data.get("phone", ""),
            lead_data.get("city", "Delhi NCR"),
            lead_data.get("state", "Uttar Pradesh"),
            lead_data.get("interested_school", "General Inquiries"),
            lead_data.get("interested_course", "B.Tech CSE / MBA / MBBS"),
            lead_data.get("source", "website_rebuild"),
            score,
            priority,
            "NEW",
            lead_data.get("notes", ""),
            lead_data.get("utm_source", "direct"),
            lead_data.get("utm_medium", "organic"),
            lead_data.get("utm_campaign", "sharda_2026_admission"),
            lead_data.get("chat_transcript", "")
        ))
        conn.commit()
        conn.close()

        logger.info(f"Saved Lead [{lead_id}] with Priority: {priority} Score: {score}")

        return {
            "lead_id": lead_id,
            "status": "success",
            "priority": priority,
            "intent_score": score,
            "message": "Student inquiry successfully registered and prioritized."
        }

    def list_leads(
        self, 
        status: Optional[str] = None, 
        priority: Optional[str] = None, 
        search: Optional[str] = None, 
        limit: int = 50, 
        offset: int = 0
    ) -> Dict[str, Any]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        query = "SELECT id, lead_id, full_name, email, phone, city, state, interested_school, interested_course, lead_source, lead_intent_score, lead_priority, status, notes, created_at FROM leads WHERE 1=1"
        params = []

        if status:
            query += " AND status = ?"
            params.append(status)
        if priority:
            query += " AND lead_priority = ?"
            params.append(priority)
        if search:
            query += " AND (full_name LIKE ? OR email LIKE ? OR phone LIKE ? OR interested_course LIKE ?)"
            s_param = f"%{search}%"
            params.extend([s_param, s_param, s_param, s_param])

        count_query = query.replace("SELECT id, lead_id, full_name, email, phone, city, state, interested_school, interested_course, lead_source, lead_intent_score, lead_priority, status, notes, created_at", "SELECT COUNT(*)")
        cur.execute(count_query, params)
        total_count = cur.fetchone()[0]

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        cur.execute(query, params)
        rows = cur.fetchall()
        conn.close()

        leads = []
        for r in rows:
            leads.append({
                "id": r[0],
                "lead_id": r[1],
                "full_name": r[2],
                "email": r[3],
                "phone": r[4],
                "city": r[5],
                "state": r[6],
                "interested_school": r[7],
                "interested_course": r[8],
                "lead_source": r[9],
                "intent_score": r[10],
                "priority": r[11],
                "status": r[12],
                "notes": r[13],
                "created_at": r[14]
            })

        return {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "leads": leads
        }

    def update_lead_status(self, lead_id: str, new_status: str, notes: Optional[str] = None) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if notes:
            cur.execute("UPDATE leads SET status = ?, notes = ?, updated_at = CURRENT_TIMESTAMP WHERE lead_id = ?", (new_status, notes, lead_id))
        else:
            cur.execute("UPDATE leads SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE lead_id = ?", (new_status, lead_id))
        updated = cur.rowcount > 0
        conn.commit()
        conn.close()
        return updated

    def get_lead_analytics(self) -> Dict[str, Any]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        
        cur.execute("SELECT COUNT(*), AVG(lead_intent_score) FROM leads")
        total_leads, avg_score = cur.fetchone()
        
        cur.execute("SELECT status, COUNT(*) FROM leads GROUP BY status")
        status_dist = {r[0]: r[1] for r in cur.fetchall()}
        
        cur.execute("SELECT lead_priority, COUNT(*) FROM leads GROUP BY lead_priority")
        priority_dist = {r[0]: r[1] for r in cur.fetchall()}

        cur.execute("SELECT interested_course, COUNT(*) FROM leads GROUP BY interested_course ORDER BY COUNT(*) DESC LIMIT 5")
        top_courses = [{"course": r[0], "count": r[1]} for r in cur.fetchall()]

        conn.close()

        return {
            "total_leads": total_leads or 0,
            "average_intent_score": round(avg_score or 0, 1),
            "status_distribution": status_dist,
            "priority_distribution": priority_dist,
            "top_requested_courses": top_courses
        }

    def export_leads_csv(self) -> str:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT lead_id, full_name, email, phone, city, state, interested_course, intent_score, priority, status, created_at FROM leads ORDER BY created_at DESC")
        rows = cur.fetchall()
        conn.close()

        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Lead ID", "Full Name", "Email", "Phone", "City", "State", "Course", "Intent Score", "Priority", "Status", "Created At"])
        for r in rows:
            writer.writerow(r)
        return output.getvalue()

crm_service = CRMLeadService()
