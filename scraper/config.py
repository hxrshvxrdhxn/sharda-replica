import os
from pathlib import Path

BASE_URL = "https://www.sharda.ac.in"
MEDIA_BASE_URL = "https://media.sharda.ac.in"

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "scraper" / "output"
RAW_PAGES_DIR = OUTPUT_DIR / "raw_pages"
MASTER_DATA_DIR = OUTPUT_DIR / "master_data"
ASSETS_DIR = BASE_DIR / "frontend" / "public" / "assets"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

KEY_URLS = [
    {"category": "home", "url": "https://www.sharda.ac.in/", "slug": "home"},
    {"category": "about", "url": "https://www.sharda.ac.in/about/overview", "slug": "about-overview"},
    {"category": "about", "url": "https://www.sharda.ac.in/about/leadership", "slug": "leadership"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions", "slug": "admissions"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions/how-to-apply", "slug": "how-to-apply"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions/fee-structure", "slug": "fee-structure"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions/scholarship", "slug": "scholarship"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions/suat", "slug": "suat"},
    {"category": "admissions", "url": "https://www.sharda.ac.in/admissions/hostel-fee", "slug": "hostel-fee"},
    {"category": "placements", "url": "https://www.sharda.ac.in/placements", "slug": "placements"},
    {"category": "placements", "url": "https://www.sharda.ac.in/placements/recruiters", "slug": "recruiters"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools", "slug": "schools-index"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/engineering-and-technology", "slug": "school-engineering"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/business-studies", "slug": "school-business"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/medical-sciences-and-research", "slug": "school-medical"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/dental-sciences", "slug": "school-dental"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/law", "slug": "school-law"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/humanities-and-social-sciences", "slug": "school-humanities"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/design", "slug": "school-design"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/allied-health-sciences", "slug": "school-allied-health"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/pharmacy", "slug": "school-pharmacy"},
    {"category": "schools", "url": "https://www.sharda.ac.in/schools/agricultural-sciences", "slug": "school-agriculture"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes", "slug": "programmes-index"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/b-tech-cse", "slug": "btech-cse"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/b-tech-cse-ai-ml", "slug": "btech-cse-aiml"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/mba", "slug": "mba"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/bba", "slug": "bba"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/mbbs", "slug": "mbbs"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/b-des", "slug": "b-des"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/b-a-llb-hons", "slug": "ba-llb"},
    {"category": "programmes", "url": "https://www.sharda.ac.in/programmes/b-pharm", "slug": "b-pharm"},
    {"category": "international", "url": "https://www.sharda.ac.in/international", "slug": "international"},
    {"category": "campus_life", "url": "https://www.sharda.ac.in/campus-life", "slug": "campus-life"},
    {"category": "contact", "url": "https://www.sharda.ac.in/contact", "slug": "contact"},
]

os.makedirs(RAW_PAGES_DIR, exist_ok=True)
os.makedirs(MASTER_DATA_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)
