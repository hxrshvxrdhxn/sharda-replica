import sqlite3
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger("CMSService")
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "sharda_pages.db"

class CMSService:
    def __init__(self):
        self._init_cms_tables()

    def _init_cms_tables(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            
            # 1. Banners Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cms_banners (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    subtitle TEXT,
                    image_url TEXT NOT NULL,
                    cta_text TEXT DEFAULT 'Apply Now',
                    cta_link TEXT DEFAULT '/admissions',
                    target_school TEXT DEFAULT 'global',
                    is_active INTEGER DEFAULT 1,
                    display_order INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 2. Announcements / Alerts Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cms_announcements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT DEFAULT 'Admissions',
                    link_url TEXT DEFAULT '/admissions',
                    is_urgent INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # 3. Dynamic FAQs Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cms_faqs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT DEFAULT 'Admissions',
                    question TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    display_order INTEGER DEFAULT 0,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Seed initial sample data if empty
            cur.execute("SELECT COUNT(*) FROM cms_banners")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO cms_banners (title, subtitle, image_url, cta_text, cta_link, target_school, display_order)
                    VALUES 
                    ('Admissions Open 2026-27', 'NAAC A+ Accredited University with up to 100% Scholarships', '/assets/imgs/home-banner2.jpg', 'Apply Now', '/admissions', 'global', 1),
                    ('School of Business Studies', 'Global Exposure & Top Tier Corporate Placements', '/assets/imgs/gallery-banner2.png', 'Explore SBS', '/schools/business-studies', 'business', 2)
                """)

            cur.execute("SELECT COUNT(*) FROM cms_announcements")
            if cur.fetchone()[0] == 0:
                cur.execute("""
                    INSERT INTO cms_announcements (title, category, link_url, is_urgent)
                    VALUES 
                    ('SUAT 2026 Online Entrance Test Booking is Live', 'Admissions', '/suat', 1),
                    ('Sharda Merit-Based Scholarships 2026 for B.Tech & MBA Applications', 'Scholarships', '/admissions/scholarship', 0),
                    ('International Student Admissions 2026 Open for 95+ Countries', 'International', '/international', 0)
                """)

            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Error initializing CMS tables: {e}")

    # Banners CRUD
    def list_banners(self, school: Optional[str] = None) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        if school:
            cur.execute("SELECT id, title, subtitle, image_url, cta_text, cta_link, target_school, is_active, display_order FROM cms_banners WHERE target_school = ? OR target_school = 'global' ORDER BY display_order ASC", (school,))
        else:
            cur.execute("SELECT id, title, subtitle, image_url, cta_text, cta_link, target_school, is_active, display_order FROM cms_banners ORDER BY display_order ASC")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "title": r[1], "subtitle": r[2], "image_url": r[3], "cta_text": r[4], "cta_link": r[5], "target_school": r[6], "is_active": bool(r[7]), "display_order": r[8]} for r in rows]

    def create_banner(self, banner_data: Dict[str, Any]) -> int:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cms_banners (title, subtitle, image_url, cta_text, cta_link, target_school, display_order)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            banner_data["title"],
            banner_data.get("subtitle", ""),
            banner_data["image_url"],
            banner_data.get("cta_text", "Apply Now"),
            banner_data.get("cta_link", "/admissions"),
            banner_data.get("target_school", "global"),
            banner_data.get("display_order", 0)
        ))
        banner_id = cur.lastrowid
        conn.commit()
        conn.close()
        return banner_id

    def delete_banner(self, banner_id: int) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM cms_banners WHERE id = ?", (banner_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    # Announcements CRUD
    def list_announcements(self) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT id, title, category, link_url, is_urgent, is_active FROM cms_announcements WHERE is_active = 1 ORDER BY id DESC")
        rows = cur.fetchall()
        conn.close()
        return [{"id": r[0], "title": r[1], "category": r[2], "link_url": r[3], "is_urgent": bool(r[4]), "is_active": bool(r[5])} for r in rows]

    def create_announcement(self, ann_data: Dict[str, Any]) -> int:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO cms_announcements (title, category, link_url, is_urgent)
            VALUES (?, ?, ?, ?)
        """, (
            ann_data["title"],
            ann_data.get("category", "General"),
            ann_data.get("link_url", "/admissions"),
            1 if ann_data.get("is_urgent") else 0
        ))
        ann_id = cur.lastrowid
        conn.commit()
        conn.close()
        return ann_id

    def delete_announcement(self, ann_id: int) -> bool:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM cms_announcements WHERE id = ?", (ann_id,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

cms_service = CMSService()
