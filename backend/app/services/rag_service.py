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
            "You are 'Sharda AI (SAI)', the official intelligence counselor for Sharda University (NAAC A+ Accredited, Greater Noida, Delhi-NCR), engineered by Turbo Bytes Consulting (TBC).\n\n"
            "STRICT RULES (CRITICAL):\n"
            "1. BE EXTREMELY SHORT, CRISP & DIRECT: Maximum 3 to 4 concise bullet points or 3-4 short sentences total. Zero conversational fluff, zero filler ('Sure', 'Here is the info', 'Welcome'). Answer immediately.\n"
            "2. BOLD KEY DATA: Highlight dates, eligibility %, annual fees, highest packages (₹1.00 Cr International, ₹45 LPA Domestic), and scholarship tiers (up to 100%).\n"
            "3. USE MINI TABLES ONLY IF COMPARING MULTIPLE PROGRAMS: Keep tables compact (3-4 columns max).\n"
            "4. ALWAYS END WITH 2-3 CLICKABLE LINK PILLS: Each on a new line in this exact format:\n"
            "   🔗 [Explore B.Tech CSE Details](/programmes/b-tech-cse)\n"
            "   🔗 [Admissions 2026 Process](/admissions)\n"
            "   🔗 [Scholarship Slabs & Calculator](/scholarships)\n"
            "   🔗 [Book SUAT 2026 Slot](/suat)\n"
            "   🔗 [Hostel Fees & Booking](/hostel)\n"
            "   🔗 [Explore MBA Programs](/programmes/mba)\n"
            "   🔗 [Medical Sciences & Research](/schools/medical-sciences-and-research)\n"
            "   🔗 [All Academic Programmes](/programmes)"
        )

        prompt = f"User Query: {query}\n\nVerified University Knowledge Context:\n{context_text}"

        candidate_models = ["gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.5-flash", "gemini-flash-latest"]
        # Remove duplicates preserving order
        seen_models = set()
        model_queue = [m for m in candidate_models if m and not (m in seen_models or seen_models.add(m))]

        if settings.GEMINI_API_KEY:
            for model_name in model_queue:
                try:
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
                    
                    # Build conversation contents
                    contents = []
                    if conversation_history:
                        for msg in conversation_history[-4:]:
                            role = "user" if msg.get("role") == "user" else "model"
                            contents.append({"role": role, "parts": [{"text": msg.get("content", "")}]})
                    
                    contents.append({
                        "role": "user",
                        "parts": [{"text": prompt}]
                    })

                    payload = {
                        "system_instruction": {
                            "parts": [{"text": system_instruction}]
                        },
                        "contents": contents,
                        "generationConfig": {
                            "temperature": 0.1,
                            "maxOutputTokens": 300
                        }
                    }
                    async with httpx.AsyncClient(timeout=10.0) as client:
                        res = await client.post(gemini_url, json=payload)
                        if res.status_code == 200:
                            data = res.json()
                            ai_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                            
                            # Ensure clickable links are present
                            if not re.search(r'\[.*?\]\(.*?\)', ai_text):
                                links_to_add = []
                                if matched_programs:
                                    for p in matched_programs[:2]:
                                        links_to_add.append(f"🔗 [{p.get('title')} Details & Fees]({p.get('url')})")
                                elif any(w in query.lower() for w in ["admission", "apply", "deadline", "close", "last date", "when"]):
                                    links_to_add.append("🔗 [Admissions 2026 Process & Application Form](/admissions)")
                                    links_to_add.append("🔗 [Book SUAT 2026 Slot](/suat)")
                                elif "scholarship" in query.lower():
                                    links_to_add.append("🔗 [Calculate Scholarship Slabs](/scholarships)")
                                elif "hostel" in query.lower():
                                    links_to_add.append("🔗 [Campus Hostels & Accommodation](/hostel)")
                                else:
                                    links_to_add.append("🔗 [Explore Academic Programmes](/programmes)")
                                    links_to_add.append("🔗 [Admissions 2026 Portal](/admissions)")
                                
                                ai_text += "\n\n" + "\n".join(links_to_add)

                            return {
                                "response": ai_text,
                                "sources": [c.get("title") for c in relevant_chunks],
                                "matched_programs": matched_programs,
                                "lead_capture_recommended": self.should_trigger_lead_capture(query),
                                "model": f"{model_name} (Turbo Bytes Consulting)",
                                "powered_by": "Turbo Bytes Consulting (TBC)"
                            }
                        else:
                            logger.warning(f"Model {model_name} returned status {res.status_code}: {res.text[:100]}")
                except Exception as e:
                    logger.warning(f"Model {model_name} failed: {e}. Trying next model...")

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

        # Admission close / dates
        if "close" in q or "deadline" in q or "last date" in q or "when" in q and "admission" in q:
            return (
                "**Admissions for 2026 at Sharda University are currently open.**\n\n"
                "- **Early Phase 1 Applications**: Ongoing now (Priority for scholarship allocation & preferred branches)\n"
                "- **SUAT 2026 Entrance Test**: Conducted continuously in online slots\n"
                "- **Final Admission Deadline**: Typically closes by **July / August 2026** prior to academic session orientation\n"
                "- **High Demand Notice**: Seats for **B.Tech CSE** and specialized AI tracks fill up quickly.\n\n"
                "🔗 [Apply Now for Admissions 2026](/admissions)\n"
                "🔗 [Book SUAT 2026 Slot](/suat)\n"
                "🔗 [View All Academic Programmes & Eligibility](/programmes)"
            )

        # Engineering / B.Tech / CSE
        if "engineering" in q or "b.tech" in q or "btech" in q or "cse" in q:
            return (
                "**B.Tech at Sharda University is NBA & NAAC A+ Accredited with up to 100% merit scholarships.**\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **B.Tech CSE (General / Core)** | 4 Years | ₹2,20,000 / yr | 10+2 PCM/CS ≥ 60% + SUAT/JEE |\n"
                "| **B.Tech CSE (AI & ML)** | 4 Years | ₹2,35,000 / yr | 10+2 PCM ≥ 60% + SUAT/JEE |\n"
                "| **B.Tech Biotechnology** | 4 Years | ₹2,05,000 / yr | 10+2 PCB/PCM ≥ 55% + SUAT |\n"
                "| **M.Tech Data Science / CSE** | 2 Years | ₹1,20,000 / yr | B.Tech/MCA ≥ 50% + GATE/SUAT |\n\n"
                "- **Placements**: ₹1.00 Crore International Highest | ₹45 LPA Domestic Highest (Amazon, Microsoft, TCS, Deloitte).\n"
                "- **Scholarships**: Up to **100% Tuition Waiver** based on 10+2 board marks / JEE rank.\n\n"
                "🔗 [Explore B.Tech CSE Details & Curriculum](/programmes/b-tech-cse)\n"
                "🔗 [Apply for 2026 B.Tech Admissions](/admissions)\n"
                "🔗 [Calculate Your Scholarship Slab](/scholarships)"
            )

        # MBA / Business
        if "mba" in q or "business" in q or "bba" in q or "management" in q:
            return (
                "**School of Business Studies (SBS) holds IACBE (USA) membership & NAAC A+ Grade.**\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **MBA (Dual Specialization)** | 2 Years | ₹3,85,000 / yr | Graduation ≥ 50% + MAT/CAT/XAT/SUAT + GD/PI |\n"
                "| **MBA (Business Analytics)** | 2 Years | ₹4,10,000 / yr | Graduation ≥ 50% + SUAT/CAT/MAT |\n"
                "| **BBA (Hons / Research)** | 3-4 Years | ₹1,85,000 / yr | 10+2 ≥ 50% + SUAT |\n\n"
                "- **Hiring Partners**: Deloitte, KPMG, EY, PwC, Amazon, HDFC Bank, ICICI.\n"
                "- **Scholarships**: Up to 100% tuition waiver for high CAT/MAT percentiles.\n\n"
                "🔗 [Explore MBA Programs & Specialisations](/programmes/mba)\n"
                "🔗 [Register for MBA GD/PI & Counseling](/admissions)"
            )

        # Biology / Bio-Science / Biotech
        if "biology" in q or "bio" in q or "botany" in q or "microbiology" in q:
            return (
                "**School of Bio-Science & Technology offers DST-FIST analytical research facilities.**\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **B.Sc. (Hons) Biotechnology** | 3-4 Years | ₹1,45,000 / yr | 10+2 PCB/PCM ≥ 50% |\n"
                "| **B.Sc. (Hons) Microbiology** | 3-4 Years | ₹1,40,000 / yr | 10+2 PCB ≥ 50% |\n"
                "| **M.Sc. Biotechnology** | 2 Years | ₹1,15,000 / yr | B.Sc. in Life Sciences ≥ 50% |\n\n"
                "🔗 [View Bio-Sciences Programs](/programmes)\n"
                "🔗 [Apply for Admissions 2026](/admissions)"
            )

        # Medical & Dental
        if "medical" in q or "mbbs" in q or "dental" in q or "bds" in q or "doctor" in q:
            return (
                "**Medical education at Sharda is anchored by a 1,200+ bed super-speciality hospital.**\n\n"
                "- **MBBS**: 5.5 Years (inc. 1 yr internship) | 250 Seats | 10+2 PCB ≥ 50% + NEET-UG (UP DGME Counseling)\n"
                "- **BDS (Dental)**: 5 Years | 100 Seats | 10+2 PCB ≥ 50% + NEET-UG\n"
                "- **MD / MS Clinical**: 3 Years | NEET-PG Qualified\n\n"
                "🔗 [SMS&R Medical Sciences Details](/schools/medical-sciences-and-research)\n"
                "🔗 [Check Medical Admission Guidelines](/admissions)"
            )

        # LLM after 12th specific check
        if ("llm" in q or "ll.m" in q) and ("12" in q or "after 12" in q or "10+2" in q or "school" in q):
            return (
                "* **No, you cannot pursue LL.M directly after 12th.** LL.M (Master of Laws) is a postgraduate degree requiring a completed Bachelor of Laws (**LL.B.**) degree with minimum 50% marks.\n"
                "* **Law Options After 12th**: You can enroll in Sharda's 5-year integrated programs: **B.A. LL.B. (Hons)** or **B.B.A. LL.B. (Hons)** at the School of Law.\n"
                "* **Eligibility**: **10+2 with minimum 50% aggregate marks** + valid score in **CLAT / LSAT / SUAT 2026**.\n"
                "* **Annual Fee**: **₹1,95,000 / yr** with up to **100% merit scholarship** tuition waivers available.\n\n"
                "🔗 [Explore Integrated Law Programmes (BA LLB / BBA LLB)](/programmes)\n"
                "🔗 [Apply Online for 2026 Admissions](/admissions)\n"
                "🔗 [Book SUAT 2026 Test Slot](/suat)"
            )

        # General Law
        if "law" in q or "llb" in q or "ll.b" in q or "llm" in q or "ll.m" in q or "ba llb" in q or "bba llb" in q:
            return (
                "**Sharda School of Law is BCI-approved with moot courts and legal aid clinics.**\n\n"
                "- **B.A. LL.B. / B.B.A. LL.B. (Integrated)**: 5 Years | ₹1,95,000 / yr | 10+2 ≥ 50% + CLAT/LSAT/SUAT\n"
                "- **LL.B. (3 Years)**: 3 Years | ₹1,75,000 / yr | Graduation ≥ 50%\n"
                "- **LL.M. (1 Year)**: 1 Year | ₹1,40,000 / yr | LL.B. ≥ 50%\n\n"
                "🔗 [Explore Law Programs](/programmes)\n"
                "🔗 [Apply Online for Law Admission](/admissions)"
            )

        # Scholarship
        if "scholarship" in q or "fee waiver" in q:
            return (
                "**Sharda University offers Merit Scholarships with up to 100% Tuition Fee Waiver:**\n\n"
                "| 10+2 Board / Score | Tuition Fee Waiver |\n"
                "| :--- | :--- |\n"
                "| **95.00% & Above** | **100% Waiver** |\n"
                "| **90.00% – 94.99%** | **50% Waiver** |\n"
                "| **85.00% – 89.99%** | **40% Waiver** |\n"
                "| **80.00% – 84.99%** | **20% Waiver** |\n"
                "| **75.00% – 79.99%** | **10% Waiver** |\n\n"
                "- *Additional Categories*: Sports Excellence (up to 100%), Defense Wards (5%), Siblings (5%).\n\n"
                "🔗 [Calculate Scholarship Eligibility](/scholarships)\n"
                "🔗 [Apply for 2026 Admissions](/admissions)"
            )

        # Hostel
        if "hostel" in q or "accommodation" in q or "room" in q or "mess" in q:
            return (
                "**Campus Hostel Accommodation (Includes 4 daily meals, Wi-Fi, Gym & Housekeeping):**\n\n"
                "- **AC 3-Seater**: ₹1,61,000 / year (+ ₹10,000 refundable security)\n"
                "- **AC 2-Seater**: ₹1,92,000 / year (+ ₹10,000 refundable security)\n"
                "- **Non-AC 3-Seater**: ₹1,16,000 / year\n"
                "- **Single Studio Apartment (AC)**: ₹2,35,000 / year\n\n"
                "🔗 [View Hostel Details & Virtual Tour](/hostel)\n"
                "🔗 [Admissions & Campus Booking](/admissions)"
            )

        if chunks:
            response_text = f"**{chunks[0].get('title')}**\n\n{chunks[0].get('content')}\n\n"
            response_text += "🔗 [Visit Admissions 2026 Portal](/admissions)\n🔗 [Explore Academic Programs](/programmes)"
            return response_text.strip()

        return (
            "**Welcome to Sharda AI Counselor (NAAC A+ Accredited).**\n\n"
            "I can assist you with quick details on:\n"
            "- **B.Tech, MBA, Medical, Law & 130+ degree courses**\n"
            "- **SUAT 2026 entrance test & application deadlines**\n"
            "- **Up to 100% merit scholarship slabs**\n"
            "- **Campus hostel fees & ₹1.00 Cr placement records**\n\n"
            "🔗 [Explore Programs Catalog](/programmes)\n"
            "🔗 [Admissions 2026 Overview](/admissions)\n"
            "🔗 [Scholarship Calculator](/scholarships)"
        )

rag_service = TurboBytesShardaBrainService()
