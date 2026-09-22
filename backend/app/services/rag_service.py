import json
import logging
import re
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
import httpx
from ..core.config import settings

logger = logging.getLogger("TurboBytesAI")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MASTER_DATA_DIR = BASE_DIR / "scraper" / "output" / "master_data"
DB_PATH = BASE_DIR / "backend" / "data" / "sharda_pages.db"

SYNONYM_EXPANSIONS = {
    "cse": ["computer science", "cse", "computing", "software", "artificial intelligence", "data science"],
    "btech": ["b.tech", "btech", "bachelor of technology", "engineering"],
    "b.tech": ["b.tech", "btech", "bachelor of technology", "engineering"],
    "mba": ["mba", "master of business", "management", "marketing", "finance", "business studies"],
    "bba": ["bba", "bachelor of business", "business administration"],
    "mbbs": ["mbbs", "medicine", "medical", "doctor", "surgery", "smsr"],
    "bds": ["bds", "dental", "dentistry", "dentist"],
    "law": ["law", "llb", "ll.b", "ba llb", "bba llb", "legal", "advocate"],
    "bio": ["biotechnology", "biology", "microbiology", "bio-science", "botany", "zoology"],
    "ai": ["artificial intelligence", "machine learning", "ai & ml", "generative ai", "robotics"],
    "aiml": ["artificial intelligence", "machine learning", "ai & ml", "ai/ml"],
    "hostel": ["hostel", "accommodation", "room", "mess", "boarding"],
    "fee": ["fee", "course fee", "tuition", "hostel fee", "charges"],
    "scholarship": ["scholarship", "fee waiver", "concession", "financial aid", "cuet scholarship"],
    "suat": ["suat", "entrance exam", "admission test", "slot booking", "sample paper"]
}

class TurboBytesShardaBrainService:
    def __init__(self):
        self.knowledge_chunks: List[Dict[str, Any]] = []
        self.programs_index: List[Dict[str, Any]] = []
        self.schools_index: List[Dict[str, Any]] = []
        self.page_index: List[Dict[str, Any]] = []
        self.load_knowledge()

    def load_knowledge(self):
        # 1. Load curated master data chunks
        kb_file = MASTER_DATA_DIR / "knowledge_chunks.json"
        if kb_file.exists():
            try:
                with open(kb_file, "r", encoding="utf-8") as f:
                    self.knowledge_chunks = json.load(f)
                logger.info(f"Loaded {len(self.knowledge_chunks)} knowledge chunks for Turbo Bytes RAG.")
            except Exception as e:
                logger.error(f"Error loading knowledge chunks: {e}")

        # 2. Load programs master data
        prog_file = MASTER_DATA_DIR / "programs.json"
        if prog_file.exists():
            try:
                with open(prog_file, "r", encoding="utf-8") as f:
                    self.programs_index = json.load(f)
                logger.info(f"Loaded {len(self.programs_index)} program definitions.")
            except Exception as e:
                logger.error(f"Error loading programs: {e}")

        # 3. Load schools master data
        sch_file = MASTER_DATA_DIR / "schools.json"
        if sch_file.exists():
            try:
                with open(sch_file, "r", encoding="utf-8") as f:
                    self.schools_index = json.load(f)
            except Exception as e:
                logger.error(f"Error loading schools: {e}")

        # 4. Index all 2,388 pages from SQLite Database
        if DB_PATH.exists():
            try:
                conn = sqlite3.connect(DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT slug, category, title, meta_description, content_text FROM pages")
                rows = cur.fetchall()
                conn.close()

                self.page_index = []
                for r in rows:
                    slug, cat, title, meta_desc, text = r
                    clean_slug = (slug or "").strip("/").lower()
                    clean_title = title or clean_slug.replace("-", " ").title()

                    item = {
                        "slug": clean_slug,
                        "category": cat or "general",
                        "title": clean_title,
                        "description": meta_desc or (text[:200] if text else ""),
                        "text": text or ""
                    }
                    self.page_index.append(item)

                    # Also add degree programme pages into programs index if not already present
                    if (cat == "programmes" or clean_slug.startswith("programmes/")) and not any(p.get("url") == f"/{clean_slug}" for p in self.programs_index):
                        self.programs_index.append({
                            "title": clean_title,
                            "school": "Sharda University",
                            "annual_fee": "Refer Programme Catalog",
                            "duration": "UG / PG / Doctoral",
                            "url": f"/{clean_slug}",
                            "badge": "ACCREDITED"
                        })

                logger.info(f"Indexed {len(self.page_index)} database pages & {len(self.programs_index)} programmes in Turbo Bytes Brain.")
            except Exception as e:
                logger.error(f"Error indexing pages from SQLite DB: {e}")

    def search_programs(self, query: str, limit: int = 6) -> List[Dict[str, Any]]:
        """Instant fuzzy / keyword program search for auto-suggest and direct discovery."""
        if not query or len(query.strip()) < 2:
            return [
                {
                    "title": "B.Tech Computer Science & Engineering (AI & ML)",
                    "school": "School of Computing Science & Engineering",
                    "annual_fee": "Rs. 2,35,000",
                    "duration": "4 Years",
                    "url": "/programmes/btech-ai-machine-learning",
                    "badge": "Top Rated"
                },
                {
                    "title": "MBA (Dual Specialization - Marketing / Finance / HR)",
                    "school": "School of Business Studies",
                    "annual_fee": "Rs. 3,85,000",
                    "duration": "2 Years",
                    "url": "/programmes/mba",
                    "badge": "IACBE Member"
                },
                {
                    "title": "MBBS - Bachelor of Medicine & Bachelor of Surgery",
                    "school": "School of Medical Sciences & Research",
                    "annual_fee": "As per UP DGME",
                    "duration": "5.5 Years",
                    "url": "/programmes/mbbs",
                    "badge": "NMC Approved"
                },
                {
                    "title": "B.Sc. Biotechnology / Microbiology",
                    "school": "School of Bio-Science & Technology",
                    "annual_fee": "Rs. 1,45,000",
                    "duration": "3 Years",
                    "url": "/programmes/bsc-biotechnology",
                    "badge": "Research Hub"
                },
                {
                    "title": "BA LL.B. (Integrated 5-Year Law)",
                    "school": "School of Law",
                    "annual_fee": "Rs. 1,95,000",
                    "duration": "5 Years",
                    "url": "/programmes/ba-llb-integrated",
                    "badge": "BCI Approved"
                },
                {
                    "title": "B.Des in Interior Design & Visual Communication",
                    "school": "School of Design",
                    "annual_fee": "Rs. 2,10,000",
                    "duration": "4 Years",
                    "url": "/programmes/b-des-interior-design",
                    "badge": "Studio Labs"
                }
            ][:limit]

        query_clean = query.lower().strip()
        query_terms = [t for t in re.findall(r'\w+', query_clean) if len(t) > 1]
        
        # Expand synonyms
        expanded_terms = set(query_terms)
        for term in query_terms:
            if term in SYNONYM_EXPANSIONS:
                expanded_terms.update(SYNONYM_EXPANSIONS[term])
        if query_clean in SYNONYM_EXPANSIONS:
            expanded_terms.update(SYNONYM_EXPANSIONS[query_clean])

        matches = []
        seen_urls = set()

        # 1. Search programs master list
        for p in self.programs_index:
            title = p.get("title", "") or p.get("name", "")
            school = p.get("school", "")
            fee = p.get("annual_fee") or p.get("fee", "Refer Page")
            duration = p.get("duration", "UG/PG")
            url = p.get("url") or f"/programmes/{p.get('slug', '')}"

            text_to_match = f"{title} {school} {duration} {url}".lower()
            score = 0

            if query_clean in title.lower():
                score += 25
            if any(term == title.lower() for term in query_terms):
                score += 30

            for t in expanded_terms:
                if t in title.lower():
                    score += 10
                elif t in text_to_match:
                    score += 4

            if score > 0 and url not in seen_urls:
                seen_urls.add(url)
                matches.append({
                    "score": score,
                    "title": title,
                    "school": school or "Sharda University",
                    "annual_fee": fee if isinstance(fee, str) else f"Rs. {fee:,}",
                    "duration": duration,
                    "url": url,
                    "badge": p.get("badge", "DEGREE")
                })

        # 2. Search database pages
        for p in self.page_index:
            title = p.get("title", "")
            slug = p.get("slug", "")
            cat = p.get("category", "")
            url = f"/{slug.lstrip('/')}"
            if url in seen_urls:
                continue

            text_to_match = f"{title} {slug} {cat}".lower()
            score = 0

            if query_clean in title.lower():
                score += 15
            for t in expanded_terms:
                if t in title.lower():
                    score += 6
                elif t in text_to_match:
                    score += 2

            if score > 0:
                seen_urls.add(url)
                matches.append({
                    "score": score,
                    "title": title,
                    "school": cat.replace("-", " ").title(),
                    "annual_fee": "Refer Page",
                    "duration": "University Portal",
                    "url": url,
                    "badge": cat.upper()
                })

        matches.sort(key=lambda x: x["score"], reverse=True)
        return matches[:limit]

    def search_knowledge(self, query: str, top_k: int = 4) -> List[Dict[str, Any]]:
        if not self.knowledge_chunks:
            return []

        query_clean = query.lower().strip()
        query_terms = re.findall(r'\w+', query_clean)
        
        expanded_terms = set(query_terms)
        for term in query_terms:
            if term in SYNONYM_EXPANSIONS:
                expanded_terms.update(SYNONYM_EXPANSIONS[term])

        scored_chunks = []

        for chunk in self.knowledge_chunks:
            score = 0
            content_lower = chunk.get("content", "").lower()
            title_lower = chunk.get("title", "").lower()
            keywords = [k.lower() for k in chunk.get("keywords", [])]

            if query_clean in title_lower:
                score += 20
            if query_clean in content_lower:
                score += 10

            for term in expanded_terms:
                if len(term) < 2:
                    continue
                if term in title_lower:
                    score += 6
                for kw in keywords:
                    if term in kw:
                        score += 4
                if term in content_lower:
                    score += 2

            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_chunks[:top_k]]

    async def generate_response(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        relevant_chunks = self.search_knowledge(query)
        matched_programs = self.search_programs(query, limit=3)
        context_text = "\n\n---\n\n".join([f"[{c.get('title')}]:\n{c.get('content')}" for c in relevant_chunks])

        system_instruction = (
            "You are 'Sharda AI (SAI)', the official Google Gemini-powered conversational counselor and knowledge assistant for Sharda University (NAAC A+ Accredited, Greater Noida, Delhi NCR), built by Turbo Bytes Consulting (TBC).\n\n"
            "BEHAVIOR & PERSONA GUIDELINES:\n"
            "1. You behave like Google Gemini, but specialized exclusively for Sharda University.\n"
            "2. When the user says greetings like 'hi', 'hello', 'hey', 'good morning', warmly welcome them to Sharda University, introduce yourself as Sharda AI powered by Turbo Bytes Consulting (TBC), and proactively offer key topics they can explore (e.g., B.Tech CSE / MBA / MBBS programs, SUAT 2026 entrance exam, up to 100% scholarships, campus hostels, 1.00 Cr highest placement, or 130+ programs across 14 Schools).\n"
            "3. When answering course, fee, or admission questions, always present structured, clean Markdown tables with Program Name, Duration, Annual Tuition Fee, Eligibility, and Career Highlights.\n"
            "4. Highlight key institutional facts: NAAC A+ Grade, 63-acre lush campus in Greater Noida, 27,000+ students from 95+ countries, 100% placement support, 1,200+ bed hospital on campus.\n"
            "5. Always be polite, structured, professional, and helpful. Use clear markdown formatting (headings, bullet points, tables)."
        )

        prompt = f"User Query: {query}\n\nVerified University Knowledge Context:\n{context_text}"

        if settings.GEMINI_API_KEY:
            try:
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.GEMINI_MODEL}:generateContent?key={settings.GEMINI_API_KEY}"
                
                # Build conversation contents if history provided
                contents = []
                if conversation_history:
                    for msg in conversation_history[-4:]:
                        role = "user" if msg.get("role") == "user" else "model"
                        contents.append({"role": role, "parts": [{"text": msg.get("content", "")}]})
                
                contents.append({
                    "role": "user",
                    "parts": [{"text": f"{system_instruction}\n\n{prompt}"}]
                })

                payload = {
                    "contents": contents,
                    "generationConfig": {
                        "temperature": 0.25,
                        "maxOutputTokens": 1024
                    }
                }
                async with httpx.AsyncClient(timeout=20.0) as client:
                    res = await client.post(gemini_url, json=payload)
                    if res.status_code == 200:
                        data = res.json()
                        ai_text = data["candidates"][0]["content"]["parts"][0]["text"]
                        return {
                            "response": ai_text,
                            "sources": [c.get("title") for c in relevant_chunks],
                            "matched_programs": matched_programs,
                            "lead_capture_recommended": self.should_trigger_lead_capture(query),
                            "model": f"{settings.GEMINI_MODEL} (Turbo Bytes Consulting)",
                            "powered_by": "Turbo Bytes Consulting (TBC)"
                        }
                    else:
                        logger.error(f"Gemini API returned status {res.status_code}: {res.text}")
            except Exception as e:
                logger.error(f"Gemini API call failed: {e}. Falling back to deterministic knowledge responder.")

        fallback_answer = self.generate_grounded_answer(query, relevant_chunks)
        return {
            "response": fallback_answer,
            "sources": [c.get("title") for c in relevant_chunks],
            "matched_programs": matched_programs,
            "lead_capture_recommended": self.should_trigger_lead_capture(query),
            "model": "Turbo Bytes Grounded Brain Engine",
            "powered_by": "Turbo Bytes Consulting (TBC)"
        }

    def should_trigger_lead_capture(self, query: str) -> bool:
        lead_triggers = ["fee", "admission", "apply", "eligibility", "scholarship", "hostel", "suat", "counselor", "placement", "seat", "contact", "course", "mba", "btech", "b.tech", "mbbs", "law"]
        return any(t in query.lower() for t in lead_triggers)

    def generate_grounded_answer(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        q = query.lower()

        # Engineering / B.Tech / CSE
        if "engineering" in q or "b.tech" in q or "btech" in q or "cse" in q:
            return (
                "### 🎓 Engineering & Technology at Sharda University (SET)\n\n"
                "Sharda University's **School of Engineering and Technology (SET)** is **NBA & NAAC A+ Accredited** and approved by AICTE.\n\n"
                "| Program | Specializations | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
                "| **B.Tech Computer Science & Engg.** | AI & ML, Cyber Security, Cloud Computing, Data Science | 4 Years | Rs. 2,20,000 | 10+2 with PCM/CS min 60% + SUAT/JEE |\n"
                "| **B.Tech CSE (AI & ML)** | Deep Learning, NLP, Generative AI, Robotics | 4 Years | Rs. 2,35,000 | 10+2 with PCM min 60% + SUAT/JEE |\n"
                "| **B.Tech Biotechnology** | Genetic Engg, Bioinformatics, Food Tech | 4 Years | Rs. 2,05,000 | 10+2 with PCB/PCM min 55% + SUAT |\n"
                "| **M.Tech CSE / Data Science** | Distributed Systems, Advanced AI, Cloud | 2 Years | Rs. 1,20,000 | B.Tech/MCA min 50% + Gate/SUAT |\n\n"
                "**Placement Highlights**:\n"
                "- Highest Global Package: **1.00 Crore INR** (Amazon / Microsoft)\n"
                "- Highest Domestic Package: **45.00 LPA**\n"
                "- Top Recruiters: *Microsoft, Amazon, Cognizant, Wipro, TCS, Deloitte, Infosys, Tech Mahindra*.\n\n"
                "💡 **Scholarships**: Up to **100% Tuition Fee Waiver** is available for students scoring 95%+ in 10+2. Would you like to check your scholarship eligibility or connect with an admissions counselor?"
            )

        # MBA / Business
        if "mba" in q or "business" in q or "bba" in q or "management" in q:
            return (
                "### 💼 Management Programs at Sharda University (SBS)\n\n"
                "The **School of Business Studies (SBS)** is a member of **IACBE (USA)** and holds **NAAC A+ accreditation**.\n\n"
                "| Program | Specializations | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- | :--- |\n"
                "| **MBA (Dual Specialization)** | Marketing, Finance, HR, Business Analytics, International Business | 2 Years | Rs. 3,85,000 | Graduation 50% + SUAT/CAT/MAT/XAT + GD/PI |\n"
                "| **MBA (Business Analytics)** | Big Data, Python for Business, Predictive Modeling | 2 Years | Rs. 4,10,000 | Graduation 50% + SUAT/CAT/MAT |\n"
                "| **BBA (Hons / Research)** | E-Commerce, Finance, Marketing, Entrepreneurship | 3-4 Years | Rs. 1,85,000 | 10+2 with 50% marks + SUAT |\n\n"
                "**Top Hiring Partners**: *Deloitte, KPMG, EY, PwC, HDFC Bank, Amazon, Flipkart, ICICI Bank*.\n\n"
                "Would you like to register for the upcoming MBA Counseling & GD/PI Round?"
            )

        # Biology / Bio-Science / Biotech
        if "biology" in q or "bio" in q or "botany" in q or "microbiology" in q:
            return (
                "### 🔬 Bio-Sciences & Biotechnology Programs\n\n"
                "The **School of Bio-Science & Technology** offers world-class research laboratories and industrial collaborations.\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **B.Sc. (Hons) Biotechnology** | 3-4 Years | Rs. 1,45,000 | 10+2 PCB/PCM with min 50% |\n"
                "| **B.Sc. (Hons) Microbiology** | 3-4 Years | Rs. 1,40,000 | 10+2 PCB with min 50% |\n"
                "| **M.Sc. Biotechnology** | 2 Years | Rs. 1,15,000 | B.Sc. in Biological Sciences 50% |\n"
                "| **M.Sc. Food Science & Tech** | 2 Years | Rs. 1,20,000 | B.Sc. Food/Life Sciences 50% |\n\n"
                "**Key Facilities**: Fermentation labs, Plant Tissue Culture, Bioinformatics Center, and DST-FIST supported analytical instruments."
            )

        # Humanities & Social Sciences
        if "humanities" in q or "arts" in q or "social" in q or "psychology" in q or "english" in q:
            return (
                "### 🎨 School of Humanities & Social Sciences (SHSS)\n\n"
                "Offering diverse liberal arts and social research disciplines.\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **BA (Hons) Psychology** | 3-4 Years | Rs. 1,25,000 | 10+2 in any stream min 50% |\n"
                "| **BA (Hons) English** | 3-4 Years | Rs. 1,15,000 | 10+2 in any stream min 50% |\n"
                "| **BA (Hons) Political Science** | 3-4 Years | Rs. 1,15,000 | 10+2 in any stream min 50% |\n"
                "| **MA Clinical Psychology** | 2 Years | Rs. 1,40,000 | BA/B.Sc. Psychology min 50% |\n\n"
                "Includes hands-on psychometric assessment labs, language labs, and community engagement initiatives."
            )

        # Medical & Dental
        if "medical" in q or "mbbs" in q or "dental" in q or "bds" in q or "doctor" in q:
            return (
                "### 🏥 Medical & Dental Sciences (SMS&R and SDS)\n\n"
                "Sharda Hospital is a **1,200+ bed NABH-accredited super-speciality hospital** on campus.\n\n"
                "| Program | Duration | Intake | Eligibility & Regulatory Body |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **MBBS** | 5.5 Years (inc. 1 yr internship) | 250 Seats | 10+2 PCB min 50% + NEET-UG Qualified (NMC) |\n"
                "| **BDS (Dental Surgery)** | 5 Years | 100 Seats | 10+2 PCB min 50% + NEET-UG Qualified (DCI) |\n"
                "| **MD / MS Clinical** | 3 Years | Various | MBBS + NEET-PG Qualified |\n"
                "| **MDS (Dental Specialities)** | 3 Years | 27 Seats | BDS + NEET-MDS Qualified |\n\n"
                "Admissions are routed through centralized UP State DGME counselling."
            )

        # Law
        if "law" in q or "llb" in q or "ll.b" in q or "ba llb" in q:
            return (
                "### ⚖️ Legal Studies at Sharda School of Law\n\n"
                "Approved by the **Bar Council of India (BCI)** with active Moot Court societies and Legal Aid clinics.\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **BA LL.B. (Integrated)** | 5 Years | Rs. 1,95,000 | 10+2 min 50% + SUAT / CLAT / LSAT |\n"
                "| **BBA LL.B. (Integrated)** | 5 Years | Rs. 1,95,000 | 10+2 min 50% + SUAT / CLAT / LSAT |\n"
                "| **LL.B. (3 Years)** | 3 Years | Rs. 1,75,000 | Graduation in any discipline min 50% |\n"
                "| **LL.M. (1 Year)** | 1 Year | Rs. 1,40,000 | LL.B. min 50% + Entrance Test |"
            )

        # Scholarship
        if "scholarship" in q or "fee waiver" in q:
            return (
                "### 🏆 Sharda University Merit Scholarships (Up to 100% Fee Waiver)\n\n"
                "| 10+2 Board Percentage / Score | Tuition Fee Waiver |\n"
                "| :--- | :--- |\n"
                "| **95.00% & Above** | **100% Tuition Fee Waiver** |\n"
                "| **90.00% to 94.99%** | **50% Tuition Fee Waiver** |\n"
                "| **85.00% to 89.99%** | **40% Tuition Fee Waiver** |\n"
                "| **80.00% to 84.99%** | **20% Tuition Fee Waiver** |\n"
                "| **75.00% to 79.99%** | **10% Tuition Fee Waiver** |\n\n"
                "*Special Category Benefits*: Sports Excellence (up to 100%), Defense/Para-military wards (5%), Sibling discount (5%), and Innovation/Idea Scholarships."
            )

        # Hostel
        if "hostel" in q or "accommodation" in q or "room" in q or "mess" in q:
            return (
                "### 🏢 Campus Hostel Accommodation & Charges\n\n"
                "- **AC 3-Seater**: Rs. 1,61,000 / year (+ Rs. 10,000 refundable security deposit)\n"
                "- **AC 2-Seater**: Rs. 1,92,000 / year (+ Rs. 10,000 refundable security deposit)\n"
                "- **Non-AC 3-Seater**: Rs. 1,16,000 / year\n"
                "- **Single Studio Apartment (AC)**: Rs. 2,35,000 / year\n\n"
                "**Amenities Included**: 4 nutritious daily meals, 24/7 Wi-Fi, laundry service, housekeeping, gym access, and biometric security."
            )

        if chunks:
            response_text = f"Here is the verified information regarding your query from Sharda University's knowledge base:\n\n"
            for c in chunks:
                response_text += f"**{c.get('title')}**\n{c.get('content')}\n\n"
            return response_text.strip()

        return (
            "Welcome to **Sharda University** (NAAC A+ Accredited).\n\n"
            "I can assist you with details regarding our 14+ Schools, 130+ UG/PG programs, annual fee structures, SUAT entrance exam, up to 100% merit scholarships, campus hostels, and placement records.\n\n"
            "What specific course or department would you like to explore?"
        )

rag_service = TurboBytesShardaBrainService()
