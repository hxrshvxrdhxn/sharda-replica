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
    "law": ["law", "llb", "ll.b", "ba llb", "bba llb", "llm", "ll.m", "legal", "advocate"],
    "llm": ["llm", "ll.m", "master of laws", "law", "postgraduate law"],
    "llb": ["llb", "ll.b", "bachelor of laws", "ba llb", "bba llb", "law"],
    "bio": ["biotechnology", "biology", "microbiology", "bio-science", "botany", "zoology"],
    "ai": ["artificial intelligence", "machine learning", "ai & ml", "generative ai", "robotics"],
    "aiml": ["artificial intelligence", "machine learning", "ai & ml", "ai/ml"],
    "hostel": ["hostel", "accommodation", "room", "mess", "boarding", "residence"],
    "fee": ["fee", "course fee", "tuition", "hostel fee", "charges", "cost", "installment"],
    "scholarship": ["scholarship", "fee waiver", "concession", "financial aid", "cuet scholarship", "discount"],
    "suat": ["suat", "entrance exam", "admission test", "slot booking", "sample paper", "syllabus"]
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

        # 4. Index all 2,395 pages from SQLite Database
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
                    "title": "BA LL.B. (Integrated 5-Year Law)",
                    "school": "School of Law",
                    "annual_fee": "Rs. 1,95,000",
                    "duration": "5 Years",
                    "url": "/programmes/ba-llb-integrated",
                    "badge": "BCI Approved"
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

    def search_knowledge(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
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
                score += 25
            if query_clean in content_lower:
                score += 15

            for term in expanded_terms:
                if len(term) < 2:
                    continue
                if term in title_lower:
                    score += 8
                for kw in keywords:
                    if term in kw:
                        score += 5
                if term in content_lower:
                    score += 3

            if score > 0:
                scored_chunks.append((score, chunk))

        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_chunks[:top_k]]

    def generate_dynamic_followups(self, query: str, answer: str) -> List[str]:
        """Generate smart, context-aware follow-up question chips."""
        q_user = query.lower()
        q_all = (query + " " + answer).lower()

        # Prioritize what the user asked
        target = q_user if len(q_user) > 5 else q_all

        if any(w in target for w in ["scholarship", "fee waiver", "concession", "waiver", "88%", "90%", "95%", "85%", "80%", "75%"]):
            return [
                "Calculate scholarship for 90%+ in 12th",
                "What are the sports & defense quota scholarships?",
                "Can tuition fee be paid in semester installments?",
                "How do I apply for SUAT 2026?"
            ]

        if any(w in target for w in ["b.tech", "btech", "cse", "computer science", "ai", "machine learning", "software", "engineering"]):
            return [
                "Compare B.Tech CSE Core vs AI & ML",
                "Calculate my B.Tech scholarship for 12th score",
                "What is the ₹1.00 Cr placement record?",
                "How do I book a SUAT 2026 test slot?"
            ]

        if any(w in target for w in ["law", "llb", "ll.b", "llm", "ll.m", "ba llb", "bba llb"]):
            return [
                "What is the SUAT Law entrance syllabus?",
                "Calculate my BA LLB scholarship for 12th marks",
                "What are the moot court & placement facilities?",
                "When do 2026 Law admissions close?"
            ]

        if any(w in target for w in ["mba", "bba", "management", "business"]):
            return [
                "What is the CAT/MAT/SUAT cutoff for MBA?",
                "Show MBA dual specialisation options",
                "What are the top recruiting companies (Amazon, Deloitte)?",
                "Calculate my MBA merit scholarship"
            ]

        if any(w in target for w in ["medical", "mbbs", "dental", "bds", "smsr", "doctor"]):
            return [
                "What is the NEET UG eligibility cutoff for MBBS?",
                "Tell me about Sharda 1,200+ bed hospital",
                "What is the BDS dental fee structure?",
                "How do UP DGME counseling rounds work?"
            ]

        if any(w in target for w in ["hostel", "room", "mess", "accommodation"]):
            return [
                "What is the 3-seater AC hostel fee?",
                "Tell me about girls hostel security & amenities",
                "What is included in the 4-time mess plan?",
                "Can I book a campus tour?"
            ]

        return [
            "When do 2026 admissions close?",
            "What are the 100% merit scholarship slabs?",
            "How do I register for SUAT 2026?",
            "Explore all 130+ UG/PG programmes"
        ]

    async def generate_response(self, query: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        relevant_chunks = self.search_knowledge(query, top_k=5)
        matched_programs = self.search_programs(query, limit=4)
        context_text = "\n\n---\n\n".join([f"[{c.get('title')}]:\n{c.get('content')}" for c in relevant_chunks])

        system_instruction = (
            "You are 'Sharda AI (SAI)', the official Senior Academic Advisor and Admissions Counselor for Sharda University (NAAC A+ Accredited, Greater Noida, Delhi-NCR), engineered by Turbo Bytes Consulting (TBC).\n\n"
            "COUNSELING PERSONA & GUIDELINES:\n"
            "1. BE CONVERSATIONAL, EMPATHETIC & DIRECT: Speak with the warmth, clarity, and authority of a top university counselor. Answer the student's question immediately in the first sentence.\n"
            "2. ACADEMIC PREREQUISITE REASONING:\n"
            "   - If a student asks to do a Postgraduate/Doctoral program (like LL.M., MBA, M.Tech, MD, Ph.D.) directly after 12th/school, explain gently that it requires prior graduation and immediately guide them to the appropriate Undergraduate route (e.g. 5-Year Integrated B.A. LL.B./B.B.A. LL.B. for Law, BBA for Management, B.Tech for Engineering, MBBS for Medicine).\n"
            "   - If a student mentions their 12th marks or entrance rank (e.g., 90% in CBSE, 85 percentile in JEE/CAT), immediately calculate and highlight their exact scholarship tuition fee waiver.\n"
            "3. CLEAN STRUCTURED FORMATTING:\n"
            "   - Use 3 to 5 clear bullet points for options and key facts.\n"
            "   - **Bold** key numbers, fees (e.g. ₹2,20,000 / yr), eligibility percentages (e.g. 60% in 10+2 PCM), deadlines, and placement highlights (₹1.00 Cr International, ₹45 LPA Domestic).\n"
            "   - If comparing courses or explaining fee tiers, use a clean markdown table.\n"
            "4. ALWAYS INCLUDE ACTIONABLE DIRECT LINK PILLS AT THE END (each on its own line):\n"
            "   🔗 [Explore Program Details & Curriculum](/programmes/...)\n"
            "   🔗 [Apply Online for Admissions 2026](/admissions)\n"
            "   🔗 [Calculate Scholarship Slabs](/scholarships)\n"
            "   🔗 [Book SUAT 2026 Test Slot](/suat)"
        )

        prompt = f"User Query: {query}\n\nVerified University Knowledge Context:\n{context_text}"

        candidate_models = ["gemini-3.1-flash-lite"]
        seen_models = set()
        model_queue = [m for m in candidate_models if m and not (m in seen_models or seen_models.add(m))]

        if settings.GEMINI_API_KEY:
            for model_name in model_queue:
                try:
                    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={settings.GEMINI_API_KEY}"
                    
                    contents = []
                    if conversation_history:
                        for msg in conversation_history[-6:]:
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
                            "temperature": 0.2,
                            "maxOutputTokens": 750
                        }
                    }
                    async with httpx.AsyncClient(timeout=2.8) as client:
                        res = await client.post(gemini_url, json=payload)
                        if res.status_code == 200:
                            data = res.json()
                            ai_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                            
                            # Clean any orphaned link emoji lines
                            ai_text = re.sub(r'(?m)^\s*🔗\s*$', '', ai_text).strip()

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

                            followups = self.generate_dynamic_followups(query, ai_text)

                            return {
                                "response": ai_text,
                                "sources": [c.get("title") for c in relevant_chunks],
                                "matched_programs": matched_programs,
                                "suggested_followups": followups,
                                "lead_capture_recommended": self.should_trigger_lead_capture(query),
                                "model": f"{model_name} (Turbo Bytes Consulting)",
                                "powered_by": "Turbo Bytes Consulting (TBC)"
                            }
                        else:
                            logger.warning(f"Model {model_name} returned status {res.status_code}: {res.text[:100]}")
                except Exception as e:
                    logger.warning(f"Model {model_name} fallback: {e}")

        fallback_answer = self.generate_grounded_answer(query, relevant_chunks)
        followups = self.generate_dynamic_followups(query, fallback_answer)

        return {
            "response": fallback_answer,
            "sources": [c.get("title") for c in relevant_chunks],
            "matched_programs": matched_programs,
            "suggested_followups": followups,
            "lead_capture_recommended": self.should_trigger_lead_capture(query),
            "model": "Turbo Bytes Grounded Brain Engine",
            "powered_by": "Turbo Bytes Consulting (TBC)"
        }

    def should_trigger_lead_capture(self, query: str) -> bool:
        lead_triggers = ["fee", "admission", "apply", "eligibility", "scholarship", "hostel", "suat", "counselor", "placement", "seat", "contact", "course", "mba", "btech", "b.tech", "mbbs", "law"]
        return any(t in query.lower() for t in lead_triggers)

    def generate_grounded_answer(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        q = query.lower()

        # LLM after 12th / Law
        if ("llm" in q or "ll.m" in q) and ("12" in q or "after 12" in q or "10+2" in q or "school" in q):
            return (
                "**No, you cannot pursue an LL.M. directly after 12th.** An LL.M. (Master of Laws) is a postgraduate degree that requires an undergraduate Bachelor of Laws (**LL.B.**) degree.\n\n"
                "**Law Options Available Right After 12th:**\n"
                "- **B.A. LL.B. (Hons.)**: 5-Year Integrated | **₹1,95,000 / year** | 10+2 ≥ 50% + CLAT/LSAT/SUAT\n"
                "- **B.B.A. LL.B. (Hons.)**: 5-Year Integrated | **₹1,95,000 / year** | 10+2 ≥ 50% + CLAT/LSAT/SUAT\n"
                "- **Key Advantages**: Save 1 full academic year compared to 3-year graduation + 3-year LLB. Includes Moot Court training & Legal Aid Clinic exposure.\n"
                "- **Scholarships**: Up to **100% Tuition Fee Waiver** available on 10+2 board scores & CLAT percentiles.\n\n"
                "🔗 [Explore Integrated Law Programmes (BA LLB / BBA LLB)](/programmes)\n"
                "🔗 [Apply Online for 2026 Admissions](/admissions)\n"
                "🔗 [Calculate Scholarship Eligibility](/scholarships)"
            )

        if "law" in q or "llb" in q or "ll.b" in q or "llm" in q or "ll.m" in q or "ba llb" in q or "bba llb" in q:
            return (
                "**Sharda School of Law is BCI-approved and accredited with NAAC A+ Grade.**\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **B.A. LL.B. (Integrated)** | 5 Years | ₹1,95,000 / yr | 10+2 ≥ 50% + CLAT/LSAT/SUAT |\n"
                "| **B.B.A. LL.B. (Integrated)** | 5 Years | ₹1,95,000 / yr | 10+2 ≥ 50% + CLAT/LSAT/SUAT |\n"
                "| **LL.B. (3 Years)** | 3 Years | ₹1,75,000 / yr | Graduation ≥ 50% |\n"
                "| **LL.M. (1 Year)** | 1 Year | ₹1,40,000 / yr | LL.B. ≥ 50% |\n\n"
                "- **Moot Courts**: Dedicated international standard courtrooms and free legal clinic.\n"
                "- **Scholarships**: Up to 100% tuition waiver on 10+2 board marks and CLAT rank.\n\n"
                "🔗 [Explore Law Programs Catalog](/programmes)\n"
                "🔗 [Apply Online for Law Admission 2026](/admissions)"
            )

        # Dynamic Scholarship & Percentage Calculator
        pct_match = re.search(r'(\d{2}(?:\.\d+)?)\s*%', q)
        if "scholarship" in q or "fee waiver" in q or "concession" in q or "waiver" in q or (pct_match and ("b.tech" in q or "btech" in q or "mba" in q or "admission" in q or "fee" in q)):
            pct_val = float(pct_match.group(1)) if pct_match else None
            calc_text = ""
            if pct_val:
                if pct_val >= 95.0:
                    slab = "**100% Tuition Fee Waiver** (Full scholarship)"
                elif pct_val >= 90.0:
                    slab = "**50% Tuition Fee Waiver**"
                elif pct_val >= 85.0:
                    slab = "**40% Tuition Fee Waiver**"
                elif pct_val >= 80.0:
                    slab = "**20% Tuition Fee Waiver**"
                elif pct_val >= 75.0:
                    slab = "**10% Tuition Fee Waiver**"
                else:
                    slab = "**Standard Merit Tier** (Additional concessions available for Sports/Defense)"
                calc_text = f"**Scholarship Assessment for {pct_val}% in 10+2 Boards:**\n- **Eligible Slab**: {slab}\n\n"

            return (
                f"{calc_text}**Sharda University Merit Scholarship Slabs (2026 Admissions):**\n\n"
                "| 10+2 Board Marks | Tuition Fee Waiver | Applicable Streams |\n"
                "| :--- | :--- | :--- |\n"
                "| **95.00% & Above** | **100% Waiver** | B.Tech, Law, BBA, Biotech, Design |\n"
                "| **90.00% – 94.99%** | **50% Waiver** | All UG Non-Medical Programs |\n"
                "| **85.00% – 89.99%** | **40% Waiver** | All UG Non-Medical Programs |\n"
                "| **80.00% – 84.99%** | **20% Waiver** | All UG Non-Medical Programs |\n"
                "| **75.00% – 79.99%** | **10% Waiver** | All UG Non-Medical Programs |\n\n"
                "- **Additional Concessions**: Sports Excellence (up to 100%), Defense Wards (5%), Sibling Concession (5%).\n\n"
                "🔗 [Apply Online for 2026 Admissions](/admissions)\n"
                "🔗 [Calculate Exact Net Fee & Slabs](/scholarships)\n"
                "🔗 [Book SUAT 2026 Test Slot](/suat)"
            )

        # Admission close / dates
        if "close" in q or "deadline" in q or "last date" in q or ("when" in q and "admission" in q):
            return (
                "**Admissions for the 2026 Academic Year at Sharda University are currently active.**\n\n"
                "- **Phase 1 Early Admissions**: Ongoing right now (offers highest priority for preferred specializations & scholarship slots)\n"
                "- **SUAT 2026 Entrance Test**: Ongoing online slot booking available daily\n"
                "- **Closing Timeline**: Admissions close in phases; high-demand tracks (B.Tech CSE, AI/ML, MBA) fill rapidly by **June / July 2026**\n"
                "- **Scholarship Slabs**: Early applicants get direct board merit consideration up to **100% tuition waiver**.\n\n"
                "🔗 [Apply Now for Admissions 2026](/admissions)\n"
                "🔗 [Book SUAT 2026 Slot](/suat)\n"
                "🔗 [View All Academic Programmes & Eligibility](/programmes)"
            )

        # Engineering / B.Tech / CSE
        if "engineering" in q or "b.tech" in q or "btech" in q or "cse" in q:
            return (
                "**School of Engineering & Technology (SET) is NBA & NAAC A+ Accredited.**\n\n"
                "| Program | Duration | Annual Fee | Eligibility |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| **B.Tech CSE (General / Core)** | 4 Years | ₹2,20,000 / yr | 10+2 PCM/CS ≥ 60% + SUAT/JEE |\n"
                "| **B.Tech CSE (AI & ML)** | 4 Years | ₹2,35,000 / yr | 10+2 PCM ≥ 60% + SUAT/JEE |\n"
                "| **B.Tech Biotechnology** | 4 Years | ₹2,05,000 / yr | 10+2 PCB/PCM ≥ 55% + SUAT |\n"
                "| **M.Tech Data Science / CSE** | 2 Years | ₹1,20,000 / yr | B.Tech/MCA ≥ 50% + GATE/SUAT |\n\n"
                "- **Placements**: **₹1.00 Crore International Highest** | **₹45 LPA Domestic Highest** (Amazon, Microsoft, TCS, Deloitte).\n"
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
                "- **Hiring Partners**: Deloitte, KPMG, EY, PwC, Amazon, HDFC Bank, ICICI Bank.\n"
                "- **Scholarships**: Up to **100% tuition waiver** for top CAT/MAT/12th scores.\n\n"
                "🔗 [Explore MBA Programs & Specialisations](/programmes/mba)\n"
                "🔗 [Register for MBA GD/PI & Counseling](/admissions)"
            )

        # Medical & Dental
        if "medical" in q or "mbbs" in q or "dental" in q or "bds" in q or "doctor" in q:
            return (
                "**Medical education at Sharda is anchored by a 1,200+ bed NABH-accredited super-speciality hospital.**\n\n"
                "- **MBBS**: 5.5 Years (inc. 1 yr internship) | 250 Seats | 10+2 PCB ≥ 50% + NEET-UG (UP DGME Counseling)\n"
                "- **BDS (Dental)**: 5 Years | 100 Seats | 10+2 PCB ≥ 50% + NEET-UG\n"
                "- **MD / MS Clinical**: 3 Years | NEET-PG Qualified\n\n"
                "🔗 [SMS&R Medical Sciences Details](/schools/medical-sciences-and-research)\n"
                "🔗 [Check Medical Admission Guidelines](/admissions)"
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
                "- *Additional Concessions*: Sports Excellence (up to 100%), Defense Wards (5%), Sibling Concession (5%).\n\n"
                "🔗 [Calculate Scholarship Eligibility](/scholarships)\n"
                "🔗 [Apply for 2026 Admissions](/admissions)"
            )

        # Hostel
        if "hostel" in q or "accommodation" in q or "room" in q or "mess" in q:
            return (
                "**Campus Hostel Accommodation (Includes 4 daily meals, Wi-Fi, Gym, Laundry & Security):**\n\n"
                "- **AC 3-Seater**: **₹1,61,000 / year** (+ ₹10,000 refundable security)\n"
                "- **AC 2-Seater**: **₹1,92,000 / year** (+ ₹10,000 refundable security)\n"
                "- **Non-AC 3-Seater**: **₹1,16,000 / year**\n"
                "- **Single Studio Apartment (AC)**: **₹2,35,000 / year**\n\n"
                "🔗 [View Hostel Details & Virtual Tour](/hostel)\n"
                "🔗 [Admissions & Campus Booking](/admissions)"
            )

        if chunks:
            response_text = f"**{chunks[0].get('title')}**\n\n{chunks[0].get('content')}\n\n"
            response_text += "🔗 [Visit Admissions 2026 Portal](/admissions)\n🔗 [Explore Academic Programs](/programmes)"
            return response_text.strip()

        return (
            "**Welcome to Sharda University AI Admissions Counselor.**\n\n"
            "I can assist you with comprehensive details regarding:\n"
            "- **130+ Degree Programs**: B.Tech, MBA, Medical (MBBS), Law (BA/BBA LLB), Design, Allied Health & Biotech\n"
            "- **Merit Scholarships**: Up to **100% tuition waiver** based on 10+2 scores and national entrance exams\n"
            "- **SUAT 2026 Entrance Exam**: Online slot booking, sample papers & syllabus\n"
            "- **Campus Life**: 1,200+ bed hospital, AC hostels, and **₹1.00 Crore global placement** highlights\n\n"
            "🔗 [Explore Programs Catalog](/programmes)\n"
            "🔗 [Admissions 2026 Overview](/admissions)\n"
            "🔗 [Scholarship Calculator](/scholarships)"
        )

rag_service = TurboBytesShardaBrainService()
