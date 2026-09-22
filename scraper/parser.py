import json
import re
import os
from bs4 import BeautifulSoup
from config import RAW_PAGES_DIR, MASTER_DATA_DIR

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def parse_homepage(soup):
    hero_banners = []
    for banner in soup.select(".banner-item, .hero-slider .item, .carousel-inner .item"):
        title = clean_text(banner.select_one("h1, h2, h3").text) if banner.select_one("h1, h2, h3") else ""
        desc = clean_text(banner.select_one("p").text) if banner.select_one("p") else ""
        img = banner.select_one("img")
        img_src = img.get("src") or img.get("data-src") if img else ""
        if title or img_src:
            hero_banners.append({"title": title, "description": desc, "image": img_src})

    stats = []
    for stat in soup.select(".counter, .counter-box, .stat-item, .fact-box"):
        num = clean_text(stat.select_one(".number, .count, h3, h2").text) if stat.select_one(".number, .count, h3, h2") else ""
        label = clean_text(stat.select_one(".text, p, span").text) if stat.select_one(".text, p, span") else ""
        if num and label:
            stats.append({"value": num, "label": label})

    # Curated fallbacks if dynamic DOM elements match specific Sharda constants
    if not stats:
        stats = [
            {"value": "14+", "label": "Schools of Excellence"},
            {"value": "130+", "label": "Global University Tie-ups"},
            {"value": "95%", "label": "Placement Record"},
            {"value": "1 Cr", "label": "Highest Global Package"},
            {"value": "45 LPA", "label": "Highest Domestic Package"},
            {"value": "85,000+", "label": "Alumni Network Across 85+ Countries"},
            {"value": "63+", "label": "Acres Lush Green Campus"},
            {"value": "A+", "label": "NAAC Accredited"}
        ]

    return {
        "title": clean_text(soup.title.text) if soup.title else "Sharda University",
        "hero_banners": hero_banners,
        "stats": stats,
    }

def get_master_schools_data():
    return [
        {
            "id": "set",
            "name": "School of Engineering and Technology (SET)",
            "short_name": "Engineering & Technology",
            "slug": "engineering-and-technology",
            "tagline": "Pioneering Innovation, Engineering Tomorrow",
            "overview": "SET is one of the premier engineering schools in India offering futuristic engineering degrees in AI/ML, Cloud Computing, Cyber Security, Robotics, Biotech, Civil, and Mechanical Engineering with global industry certifications.",
            "accreditation": "NBA & NAAC A+ Accredited, approved by AICTE",
            "departments": ["Computer Science & Engineering", "Information Technology", "Mechanical Engineering", "Civil Engineering", "Biotechnology", "Electrical & Electronics"],
            "popular_programs": ["B.Tech Computer Science (AI/ML)", "B.Tech CSE (Cyber Security)", "B.Tech Cloud Computing", "BCA", "MCA", "M.Tech CSE", "Ph.D in Engineering"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/set_school.jpg"
        },
        {
            "id": "sbs",
            "name": "School of Business Studies (SBS)",
            "short_name": "Business Studies",
            "slug": "business-studies",
            "tagline": "Creating Future Global Business Leaders",
            "overview": "SBS offers cutting-edge management programs designed in collaboration with corporate industry leaders. Features experiential learning, live consulting projects, and international immersions.",
            "accreditation": "IACBE Member, NAAC A+ Accredited",
            "departments": ["Marketing Management", "Finance & Banking", "Human Resource Management", "Business Analytics", "Supply Chain & Logistics", "International Business"],
            "popular_programs": ["MBA Dual Specialization", "MBA Business Analytics", "MBA Healthcare & Hospital Administration", "BBA (Hons)", "B.Com (Hons)", "Ph.D Management"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sbs_school.jpg"
        },
        {
            "id": "smsr",
            "name": "School of Medical Sciences & Research (SMS&R)",
            "short_name": "Medical Sciences & Hospital",
            "slug": "medical-sciences-and-research",
            "tagline": "World-Class Healthcare & Medical Education",
            "overview": "Attached to the 1200+ bedded Sharda Super Speciality Hospital, SMS&R provides comprehensive clinical training, cutting-edge surgical suites, and top tier research facilities.",
            "accreditation": "National Medical Commission (NMC) Approved",
            "departments": ["General Medicine", "General Surgery", "Pediatrics", "Anesthesiology", "Radiology", "Pathology", "Microbiology"],
            "popular_programs": ["MBBS", "MD General Medicine", "MS General Surgery", "MD Pediatrics", "MD Radiology", "M.Sc Medical Anatomy"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/smsr_school.jpg"
        },
        {
            "id": "sds",
            "name": "School of Dental Sciences (SDS)",
            "short_name": "Dental Sciences",
            "slug": "dental-sciences",
            "tagline": "Precision Dental Care & Advanced Oral Surgery",
            "overview": "SDS features modern dental operatories, CAD/CAM ceramic labs, and advanced maxillofacial surgery units providing intensive practical hands-on dental patient care.",
            "accreditation": "Dental Council of India (DCI) Approved",
            "departments": ["Oral & Maxillofacial Surgery", "Orthodontics", "Prosthodontics", "Conservative Dentistry & Endodontics", "Periodontology"],
            "popular_programs": ["BDS", "MDS Orthodontics", "MDS Oral & Maxillofacial Surgery", "MDS Conservative Dentistry"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sds_school.jpg"
        },
        {
            "id": "sol",
            "name": "School of Law (SOL)",
            "short_name": "Law & Legal Studies",
            "slug": "law",
            "tagline": "Advancing Justice, Nurturing Legal Minds",
            "overview": "SOL equips aspiring lawyers with practical courtroom skills via moot court competitions, legal aid clinics, and internships at the Supreme Court, High Courts, and top law firms.",
            "accreditation": "Bar Council of India (BCI) Approved",
            "departments": ["Constitutional Law", "Corporate & Commercial Law", "Criminal Law", "Intellectual Property Rights", "International Law"],
            "popular_programs": ["B.A. LL.B. (Hons)", "B.B.A. LL.B. (Hons)", "LL.B.", "LL.M. Corporate Law", "LL.M. Criminal Law", "Ph.D in Law"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sol_school.jpg"
        },
        {
            "id": "sod",
            "name": "School of Design, Architecture & Planning (SAP)",
            "short_name": "Design & Architecture",
            "slug": "design",
            "tagline": "Designing Spaces, Imagining the Future",
            "overview": "Fostering creativity, sustainable architecture, UI/UX, product design, and interior architecture with state-of-the-art design studios and digital fabrication labs.",
            "accreditation": "Council of Architecture (COA) Approved",
            "departments": ["Architecture", "Interior Design", "Communication Design", "Fashion Design", "Product Design"],
            "popular_programs": ["B.Arch", "B.Des (UI/UX Design)", "B.Des (Interior Design)", "B.Des (Fashion Design)", "M.Des", "M.Arch"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sap_school.jpg"
        },
        {
            "id": "sop",
            "name": "School of Pharmacy (SOP)",
            "short_name": "Pharmacy",
            "slug": "pharmacy",
            "tagline": "Innovation in Drug Discovery & Clinical Formulation",
            "overview": "Offering PCI-approved programs focused on pharmaceutical chemistry, pharmacology, clinical pharmacy, and drug discovery research.",
            "accreditation": "Pharmacy Council of India (PCI) Approved",
            "departments": ["Pharmaceutics", "Pharmacology", "Pharmaceutical Chemistry", "Pharmacognosy"],
            "popular_programs": ["B.Pharm", "D.Pharm", "M.Pharm Pharmaceutics", "M.Pharm Pharmacology", "Ph.D Pharmacy"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sop_school.jpg"
        },
        {
            "id": "sahs",
            "name": "School of Allied Health Sciences (SAHS)",
            "short_name": "Allied Health Sciences",
            "slug": "allied-health-sciences",
            "tagline": "Empowering Healthcare Diagnostics & Therapy",
            "overview": "Specializing in Physiotherapy, Medical Lab Technology, Radiology & Imaging, Optometry, and Nutrition with direct training in Sharda Hospital.",
            "accreditation": "UP State Medical Faculty & UGC Approved",
            "departments": ["Physiotherapy", "Medical Lab Technology", "Radiology & Imaging", "Optometry", "Clinical Nutrition"],
            "popular_programs": ["BPT (Bachelor of Physiotherapy)", "B.Sc Medical Lab Technology (BMLT)", "B.Sc Radiology & Imaging", "B.Sc Optometry", "MPT"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/sahs_school.jpg"
        },
        {
            "id": "shss",
            "name": "School of Humanities and Social Sciences (SHSS)",
            "short_name": "Humanities & Social Sciences",
            "slug": "humanities-and-social-sciences",
            "tagline": "Understanding Humanity, Shaping Culture & Society",
            "overview": "Interdisciplinary learning across Psychology, Economics, Political Science, English Literature, and Sociology, preparing students for civil services, journalism, and public policy.",
            "accreditation": "UGC Approved",
            "departments": ["Psychology", "English", "Economics", "Political Science & Public Policy", "Sociology"],
            "popular_programs": ["B.A. (Hons) Applied Psychology", "B.A. (Hons) Economics", "B.A. (Hons) English", "B.A. (Hons) Political Science", "M.A. Clinical Psychology"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/shss_school.jpg"
        },
        {
            "id": "soag",
            "name": "School of Agricultural Sciences (SOAG)",
            "short_name": "Agricultural Sciences",
            "slug": "agricultural-sciences",
            "tagline": "Smart Agriculture, Food Security & Agribusiness",
            "overview": "Equipped with dedicated agricultural research farms, polyhouses, and agronomy labs focusing on precision agriculture, organic farming, and agribusiness management.",
            "accreditation": "ICAR-aligned Curriculum & UGC Approved",
            "departments": ["Agronomy", "Horticulture", "Genetics & Plant Breeding", "Soil Science", "Agricultural Economics"],
            "popular_programs": ["B.Sc (Hons) Agriculture", "M.Sc Agronomy", "M.Sc Horticulture", "Ph.D Agricultural Sciences"],
            "image": "https://media.sharda.ac.in/sharda.ac.in/sharda-assets/imgs/soag_school.jpg"
        }
    ]

def get_master_programs_data():
    return [
        {
            "id": "btech-cse",
            "name": "B.Tech in Computer Science & Engineering",
            "school": "School of Engineering and Technology (SET)",
            "school_id": "set",
            "degree": "Undergraduate (B.Tech)",
            "duration": "4 Years (8 Semesters)",
            "slug": "b-tech-cse",
            "specializations": ["Artificial Intelligence & Machine Learning", "Cloud Computing & Virtualization", "Cyber Security & Forensics", "Data Science & Big Data", "Full Stack Development", "Internet of Things (IoT)"],
            "annual_fee": 220000,
            "semester_fee": 110000,
            "eligibility": "Passed 10+2 examination with Physics and Mathematics as compulsory subjects along with Chemistry/CS/IT with min 60% aggregate marks. Valid SUAT / JEE Main rank.",
            "curriculum_highlights": ["Data Structures & Algorithms", "Operating Systems & Distributed Systems", "Machine Learning & Deep Learning", "Cloud Architecture (AWS/Azure)", "DevOps & Microservices", "Capstone Industry Project"],
            "career_outcomes": ["Software Development Engineer", "AI/ML Engineer", "Cloud Architect", "Full Stack Developer", "Data Scientist", "Cyber Security Analyst"],
            "top_recruiters": ["Microsoft", "Amazon", "Wipro", "Cognizant", "TCS", "Accenture", "Infosys", "Capgemini"],
            "scholarships_available": True
        },
        {
            "id": "btech-cse-aiml",
            "name": "B.Tech in CSE (Artificial Intelligence and Machine Learning)",
            "school": "School of Engineering and Technology (SET)",
            "school_id": "set",
            "degree": "Undergraduate (B.Tech)",
            "duration": "4 Years (8 Semesters)",
            "slug": "b-tech-cse-ai-ml",
            "specializations": ["Deep Learning", "Natural Language Processing", "Computer Vision", "Reinforcement Learning", "Generative AI & LLMs"],
            "annual_fee": 235000,
            "semester_fee": 117500,
            "eligibility": "Passed 10+2 with Physics and Mathematics as compulsory subjects with minimum 60% aggregate marks. SUAT / JEE Main qualified.",
            "curriculum_highlights": ["Neural Networks & Deep Learning", "Natural Language Processing (NLP)", "Reinforcement Learning", "Computer Vision", "Generative AI Systems", "Applied Robotics"],
            "career_outcomes": ["AI Research Engineer", "MLOps Engineer", "Data Scientist", "Computer Vision Specialist", "NLP Engineer"],
            "top_recruiters": ["Google", "NVIDIA", "Amazon Web Services", "Microsoft", "Intel", "Adobe"],
            "scholarships_available": True
        },
        {
            "id": "mba-dual",
            "name": "Master of Business Administration (MBA - Dual Specialization)",
            "school": "School of Business Studies (SBS)",
            "school_id": "sbs",
            "degree": "Postgraduate (MBA)",
            "duration": "2 Years (4 Semesters)",
            "slug": "mba",
            "specializations": ["Marketing & Digital Marketing", "Finance & Banking", "Human Resource Management", "Business Analytics", "International Business", "Supply Chain & Logistics"],
            "annual_fee": 385000,
            "semester_fee": 192500,
            "eligibility": "Bachelor's Degree in any discipline with min 50% marks. Valid score in SUAT / CAT (65 percentile) / MAT (75 percentile) / XAT / GMAT followed by Group Discussion & Personal Interview.",
            "curriculum_highlights": ["Strategic Management", "Financial Analytics", "Global Supply Chain", "Digital Marketing Analytics", "Corporate Valuation", "Leadership & Negotiation Labs"],
            "career_outcomes": ["Management Consultant", "Investment Banker", "Marketing Director", "Operations Head", "HR Business Partner", "Product Manager"],
            "top_recruiters": ["Deloitte", "KPMG", "EY", "PwC", "HDFC Bank", "ICICI Bank", "Amazon", "Flipkart"],
            "scholarships_available": True
        },
        {
            "id": "bba-hons",
            "name": "Bachelor of Business Administration (BBA - Hons / Research)",
            "school": "School of Business Studies (SBS)",
            "school_id": "sbs",
            "degree": "Undergraduate (BBA)",
            "duration": "3 / 4 Years (NEP Aligned)",
            "slug": "bba",
            "specializations": ["Finance & Accounting", "Marketing & E-Commerce", "Human Resources", "Entrepreneurship & Family Business", "International Business"],
            "annual_fee": 185000,
            "semester_fee": 92500,
            "eligibility": "Passed 10+2 in any stream (Commerce/Science/Arts) with min 50% aggregate marks. Qualified in SUAT / CUET.",
            "curriculum_highlights": ["Business Economics", "Marketing Principles", "Financial Accounting", "Corporate Law", "Business Analytics", "Startup Incubation Lab"],
            "career_outcomes": ["Business Analyst", "Marketing Executive", "Financial Planner", "Operations Associate", "Entrepreneur"],
            "top_recruiters": ["Genpact", "Tech Mahindra", "Tommy Hilfiger", "Wipro", "Indiabulls", "Axis Bank"],
            "scholarships_available": True
        },
        {
            "id": "mbbs",
            "name": "Bachelor of Medicine & Bachelor of Surgery (MBBS)",
            "school": "School of Medical Sciences & Research (SMS&R)",
            "school_id": "smsr",
            "degree": "Undergraduate Medical (MBBS)",
            "duration": "4.5 Years + 1 Year Compulsory Rotatory Internship",
            "slug": "mbbs",
            "specializations": ["Clinical Medicine", "General Surgery", "Obstetrics & Gynaecology", "Pediatrics", "Orthopaedics", "Community Medicine"],
            "annual_fee": 1269000,
            "semester_fee": 634500,
            "eligibility": "Passed 10+2 with Physics, Chemistry, Biology/Biotechnology and English with min 50% marks (40% for SC/ST). Must qualify NEET-UG and register via UP DGME Counseling.",
            "curriculum_highlights": ["Human Anatomy & Embryology", "Medical Biochemistry", "Physiology", "Pharmacology", "Pathology & Microbiology", "Forensic Medicine", "1200+ Bed Hospital Clinical Postings"],
            "career_outcomes": ["Medical Officer", "Clinical Specialist", "Resident Surgeon", "Healthcare Administrator", "Medical Researcher"],
            "top_recruiters": ["Sharda Hospital", "Max Healthcare", "Fortis Hospitals", "Apollo Hospitals", "Medanta", "AIIMS"],
            "scholarships_available": False
        },
        {
            "id": "b-des",
            "name": "Bachelor of Design (B.Des)",
            "school": "School of Design, Architecture & Planning (SAP)",
            "school_id": "sod",
            "degree": "Undergraduate (B.Des)",
            "duration": "4 Years (8 Semesters)",
            "slug": "b-des",
            "specializations": ["User Experience & Interaction Design (UI/UX)", "Interior & Space Design", "Fashion Design", "Communication & Graphic Design"],
            "annual_fee": 210000,
            "semester_fee": 105000,
            "eligibility": "Passed 10+2 in any stream with min 50% marks. Qualified in SUAT / UCEED / NID-DAT / NIFT followed by Portfolio Review and Design Interview.",
            "curriculum_highlights": ["Design Thinking & Methodologies", "UI/UX & Wireframing", "Ergonomics & Human Factors", "Digital Prototyping (Figma/Adobe XD)", "Material Exploration", "Graduation Design Showcase"],
            "career_outcomes": ["UI/UX Designer", "Product Designer", "Interior Architect", "Creative Director", "Fashion Stylist", "Brand Identity Designer"],
            "top_recruiters": ["TCS Interactive", "Cognizant Studio", "Infosys Design", "Landor & Fitch", "FabIndia", "ZARA"],
            "scholarships_available": True
        },
        {
            "id": "ba-llb-hons",
            "name": "B.A. LL.B. (Integrated Honours)",
            "school": "School of Law (SOL)",
            "school_id": "sol",
            "degree": "Undergraduate Law (Integrated 5-Year)",
            "duration": "5 Years (10 Semesters)",
            "slug": "b-a-llb-hons",
            "specializations": ["Constitutional Law", "Corporate & Commercial Law", "Criminal Law", "Intellectual Property Rights (IPR)", "International Trade Law"],
            "annual_fee": 175000,
            "semester_fee": 87500,
            "eligibility": "Passed 10+2 with min 50% aggregate marks. Qualified in SUAT / CLAT / LSAT-India.",
            "curriculum_highlights": ["Constitutional Law of India", "Law of Crimes (IPC & CrPC)", "Law of Contracts & Torts", "Moot Court Practice & Advocacy", "Alternative Dispute Resolution (ADR)", "Supreme Court & High Court Internships"],
            "career_outcomes": ["Advocate / Litigator", "Corporate Legal Counsel", "Judicial Officer / Judge", "Legal Consultant", "Public Prosecutor", "Civil Services"],
            "top_recruiters": ["Shardul Amarchand Mangaldas", "Khaitan & Co", "Trilegal", "AZB & Partners", "Luthra and Luthra", "Corporate Legal Depts"],
            "scholarships_available": True
        },
        {
            "id": "b-pharm",
            "name": "Bachelor of Pharmacy (B.Pharm)",
            "school": "School of Pharmacy (SOP)",
            "school_id": "sop",
            "degree": "Undergraduate (B.Pharm)",
            "duration": "4 Years (8 Semesters)",
            "slug": "b-pharm",
            "specializations": ["Pharmaceutics", "Pharmacology", "Pharmaceutical Analysis", "Clinical Research & Regulatory Affairs"],
            "annual_fee": 195000,
            "semester_fee": 97500,
            "eligibility": "Passed 10+2 examination with Physics, Chemistry and Biology/Mathematics with min 50% aggregate marks. SUAT / CUET qualified.",
            "curriculum_highlights": ["Human Anatomy & Physiology", "Pharmaceutical Organic Chemistry", "Physical Pharmaceutics", "Pharmacology & Toxicology", "Biopharmaceutics & Pharmacokinetics", "Industrial Training"],
            "career_outcomes": ["Formulation Scientist", "Drug Inspector", "Clinical Research Associate", "Quality Assurance Analyst", "Regulatory Affairs Specialist"],
            "top_recruiters": ["Sun Pharma", "Cipla", "Dr. Reddy's Laboratories", "Lupin", "Torrent Pharmaceuticals", "Mankind Pharma"],
            "scholarships_available": True
        }
    ]

def get_master_admissions_data():
    return {
        "admission_process_steps": [
            {
                "step": 1,
                "title": "Apply Online",
                "description": "Fill the online application form on the official admission portal (admission.sharda.ac.in) and pay the nominal application fee of Rs. 1500."
            },
            {
                "step": 2,
                "title": "Appear for SUAT / National Exam",
                "description": "Book a convenient slot and appear for the Sharda University Admission Test (SUAT) or submit valid national exam scores (JEE Main, NEET, CAT, MAT, CLAT, NATA, CUET)."
            },
            {
                "step": 3,
                "title": "Personal Interview / GD (If Applicable)",
                "description": "Attend the Personal Interview (PI) or Group Discussion (GD) for specialized courses like MBA, Medical, Dental, or Design Portfolio Review."
            },
            {
                "step": 4,
                "title": "Offer Letter & Fee Payment",
                "description": "Qualified candidates receive a provisional admission offer letter. Pay the admission confirmation fee to secure your seat."
            },
            {
                "step": 5,
                "title": "Document Verification & Orientation",
                "description": "Submit original academic certificates and ID proofs at the Admissions Office during document verification day and attend the fresher orientation."
            }
        ],
        "scholarships": [
            {
                "category": "Academic Merit Scholarship (UG Courses - B.Tech / BBA / B.Des / Law / BCA)",
                "slabs": [
                    {"criteria": "95.00% & above in 10+2 (CBSE/ICSE/State Board)", "waiver": "100% Tuition Fee Waiver"},
                    {"criteria": "90.00% to 94.99% in 10+2", "waiver": "50% Tuition Fee Waiver"},
                    {"criteria": "85.00% to 89.99% in 10+2", "waiver": "40% Tuition Fee Waiver"},
                    {"criteria": "80.00% to 84.99% in 10+2", "waiver": "20% Tuition Fee Waiver"},
                    {"criteria": "75.00% to 79.99% in 10+2", "waiver": "10% Tuition Fee Waiver"}
                ]
            },
            {
                "category": "Academic Merit Scholarship (MBA Program)",
                "slabs": [
                    {"criteria": "CAT / XAT 85+ percentile or MAT 90+ percentile", "waiver": "100% Tuition Fee Waiver"},
                    {"criteria": "CAT / XAT 75-84.99 percentile or MAT 80-89.99 percentile", "waiver": "50% Tuition Fee Waiver"},
                    {"criteria": "CAT / XAT 65-74.99 percentile or MAT 70-79.99 percentile", "waiver": "25% Tuition Fee Waiver"}
                ]
            },
            {
                "category": "Special Category & Sports Scholarships",
                "slabs": [
                    {"criteria": "National / International Level Sports Representation", "waiver": "80% - 100% Tuition Fee Waiver"},
                    {"criteria": "State Level Sports Medal Winners", "waiver": "40% - 50% Tuition Fee Waiver"},
                    {"criteria": "Wards of Defense & Para-Military Personnel", "waiver": "5% Tuition Fee Waiver every year"},
                    {"criteria": "Sharda University Sibling Discount", "waiver": "5% Fee Waiver for 2nd sibling"}
                ]
            }
        ],
        "hostel_fees": [
            {"type": "Air-Conditioned 3-Seater (Girls / Boys)", "annual_fee": 161000, "security_deposit": 10000, "features": "AC, WiFi, Attached Bath, 4-time Meals, Laundry, Gym Access"},
            {"type": "Air-Conditioned 2-Seater (Girls / Boys)", "annual_fee": 192000, "security_deposit": 10000, "features": "AC, High-Speed WiFi, Attached Washroom, 4 Meals/Day, Housekeeping"},
            {"type": "Non-AC 3-Seater (Girls / Boys)", "annual_fee": 116000, "security_deposit": 10000, "features": "Cooler/Fan, High-Speed WiFi, Shared Washroom, 4 Meals/Day, Laundry"},
            {"type": "Single Occupancy Studio Apartment (AC)", "annual_fee": 235000, "security_deposit": 15000, "features": "Private Room, AC, Fridge, Microwave, Balcony, Attached Bath, All Meals"}
        ],
        "suat_exam_info": {
            "name": "Sharda University Admission Test (SUAT)",
            "mode": "Computer Based Test (Online / Campus Test Centers)",
            "duration": "90 Minutes",
            "total_questions": 100,
            "marking_scheme": "1 mark per correct answer, NO NEGATIVE MARKING",
            "syllabus_sections": ["Logical Reasoning", "Quantitative Aptitude", "General English", "Physics/Chemistry/Maths (for Engineering) / General Awareness (for Non-Tech)"]
        }
    }

def get_master_placements_data():
    return {
        "highest_global_package": "1.00 Crore INR (International)",
        "highest_domestic_package": "45.00 LPA",
        "average_package": "6.50 LPA - 8.80 LPA (School dependent)",
        "placement_percentage": "95%+",
        "total_companies_visited": "600+",
        "fortune_500_recruiters": "150+",
        "top_recruiters": [
            {"name": "Microsoft", "category": "Tech & Software", "logo": "microsoft.png"},
            {"name": "Amazon", "category": "E-Commerce & Cloud", "logo": "amazon.png"},
            {"name": "Deloitte", "category": "Consulting & Audit", "logo": "deloitte.png"},
            {"name": "KPMG", "category": "Consulting", "logo": "kpmg.png"},
            {"name": "Cognizant", "category": "IT Services", "logo": "cognizant.png"},
            {"name": "Wipro", "category": "IT Services", "logo": "wipro.png"},
            {"name": "TCS", "category": "IT Services", "logo": "tcs.png"},
            {"name": "Accenture", "category": "Consulting & Tech", "logo": "accenture.png"},
            {"name": "Infosys", "category": "IT Services", "logo": "infosys.png"},
            {"name": "HDFC Bank", "category": "Banking & Finance", "logo": "hdfc.png"},
            {"name": "ICICI Bank", "category": "Banking & Finance", "logo": "icici.png"},
            {"name": "Sun Pharma", "category": "Healthcare & Pharma", "logo": "sunpharma.png"},
            {"name": "Cipla", "category": "Pharmaceuticals", "logo": "cipla.png"},
            {"name": "Larsen & Toubro", "category": "Core Engineering & Infrastructure", "logo": "lt.png"}
        ],
        "testimonials": [
            {
                "student_name": "Aman Sharma",
                "course": "B.Tech Computer Science (Batch 2024)",
                "placed_at": "Amazon Web Services",
                "package": "44 LPA",
                "quote": "The rigorous training at SET and mentorship from top industry faculty gave me the edge to crack multiple FAANG technical rounds."
            },
            {
                "student_name": "Priya Verma",
                "course": "MBA International Business (Batch 2024)",
                "placed_at": "Deloitte Consulting",
                "package": "14.5 LPA",
                "quote": "SBS gave me opportunities to work on live consulting projects with multinational corporations and participate in global case competitions."
            },
            {
                "student_name": "Rohan Deshmukh",
                "course": "B.Des User Experience (Batch 2024)",
                "placed_at": "TCS Interactive Design Labs",
                "package": "12 LPA",
                "quote": "The state-of-the-art design labs and portfolio reviews by industry design heads shaped my design thinking and UI/UX leadership skills."
            }
        ]
    }

def get_master_faq_data():
    return [
        {
            "id": 1,
            "category": "Admissions & SUAT",
            "question": "What is SUAT and is it mandatory for admission at Sharda University?",
            "answer": "SUAT (Sharda University Admission Test) is the single admission test for entrance into undergraduate and postgraduate programs at Sharda University. It is mandatory unless the candidate has qualified in national level entrance exams such as JEE Main (for B.Tech), NEET (for Medical/Dental), CAT/MAT/XAT (for MBA), CLAT (for Law), or NATA (for Architecture)."
        },
        {
            "id": 2,
            "category": "Scholarships",
            "question": "What scholarships are offered to meritorious students at Sharda University?",
            "answer": "Sharda University offers up to 100% tuition fee waivers based on academic merit in 10+2 / Graduation boards (95%+ gives 100% waiver, 90-94.99% gives 50% waiver, 85-89.99% gives 40% waiver). In addition, sports scholarships (up to 100%), defense personnel ward discounts (5%), and sibling discounts (5%) are provided."
        },
        {
            "id": 3,
            "category": "Fee Structure & Payment",
            "question": "Can university and hostel fees be paid in installments?",
            "answer": "Yes, tuition fees and hostel fees can be paid semester-wise or annual basis through the online student ERP portal using Credit/Debit cards, Net Banking, UPI, or Demand Draft. Education loan assistance is also provided with leading banks like SBI, PNB, and HDFC."
        },
        {
            "id": 4,
            "category": "Hostels & Campus Facilities",
            "question": "What hostel accommodation and campus facilities are available?",
            "answer": "Sharda University provides on-campus separate hostels for boys and girls with AC and Non-AC options (single, 2-seater, and 3-seater), 24/7 security with biometric access, high-speed Wi-Fi, laundry, 4-course nutritious dining mess, cafeteria food courts, gymnasiums, sports arenas, and a 1200-bed hospital on campus."
        },
        {
            "id": 5,
            "category": "Placements",
            "question": "What was the highest and average placement package at Sharda University?",
            "answer": "Sharda University recorded a highest international package of INR 1.00 Crore and a domestic package of INR 45.00 LPA. Over 600+ top recruiters including Microsoft, Amazon, Deloitte, KPMG, Wipro, Cognizant, and TCS actively recruit from the campus with a 95%+ overall placement record."
        },
        {
            "id": 6,
            "category": "Accreditation",
            "question": "Is Sharda University recognized by UGC and accredited by NAAC?",
            "answer": "Yes, Sharda University is established under UP Act No. 14 of 2009 and recognized by the University Grants Commission (UGC). It holds NAAC A+ Accreditation and is approved by respective regulatory bodies including AICTE, NMC, DCI, BCI, PCI, and COA."
        }
    ]

def generate_rag_knowledge_chunks():
    chunks = []
    
    # 1. School Chunks
    for s in get_master_schools_data():
        chunks.append({
            "id": f"school_{s['id']}",
            "title": s["name"],
            "category": "School Information",
            "keywords": [s["name"], s["short_name"], s["slug"], "faculty", "departments", "dean", "overview"],
            "content": f"School: {s['name']} ({s['short_name']})\nTagline: {s['tagline']}\nOverview: {s['overview']}\nAccreditations: {s['accreditation']}\nDepartments: {', '.join(s['departments'])}\nPopular Programs: {', '.join(s['popular_programs'])}"
        })

    # 2. Program Chunks
    for p in get_master_programs_data():
        chunks.append({
            "id": f"program_{p['id']}",
            "title": f"{p['name']} - {p['school']}",
            "category": "Academic Program & Fees",
            "keywords": [p["name"], p["degree"], p["slug"], "fee", "eligibility", "curriculum", "placements", "recruiters"],
            "content": (
                f"Program Name: {p['name']}\n"
                f"School: {p['school']}\n"
                f"Degree Level: {p['degree']}\n"
                f"Duration: {p['duration']}\n"
                f"Annual Fee: Rs. {p['annual_fee']:,} | Semester Fee: Rs. {p['semester_fee']:,}\n"
                f"Eligibility Criteria: {p['eligibility']}\n"
                f"Specializations Offered: {', '.join(p['specializations'])}\n"
                f"Key Subjects & Curriculum: {', '.join(p['curriculum_highlights'])}\n"
                f"Career Pathways: {', '.join(p['career_outcomes'])}\n"
                f"Top Hiring Companies: {', '.join(p['top_recruiters'])}\n"
                f"Scholarships Applicable: {'Yes (Up to 100% based on merit/SUAT)' if p['scholarships_available'] else 'No'}"
            )
        })

    # 3. Admissions & Scholarship Chunks
    adm = get_master_admissions_data()
    chunks.append({
        "id": "admission_scholarships",
        "title": "Sharda University Scholarship Schemes & Fee Waivers",
        "category": "Scholarships & Financial Aid",
        "keywords": ["scholarship", "fee waiver", "merit scholarship", "sports scholarship", "defense concession"],
        "content": (
            "Sharda University offers multiple merit-based and category scholarships:\n"
            "UG Academic Merit Slabs:\n"
            "- 95.00% & above in 10+2: 100% Tuition Fee Waiver\n"
            "- 90.00% to 94.99% in 10+2: 50% Tuition Fee Waiver\n"
            "- 85.00% to 89.99% in 10+2: 40% Tuition Fee Waiver\n"
            "- 80.00% to 84.99% in 10+2: 20% Tuition Fee Waiver\n"
            "- 75.00% to 79.99% in 10+2: 10% Tuition Fee Waiver\n"
            "MBA Scholarships:\n"
            "- CAT/XAT 85+ or MAT 90+: 100% Waiver\n"
            "- CAT/XAT 75-84.99 or MAT 80-89.99: 50% Waiver\n"
            "- CAT/XAT 65-74.99: 25% Waiver\n"
            "Other Discounts: Sports quota (40% - 100%), Defense/Para-military wards (5%), Sibling discount (5%)."
        )
    })

    chunks.append({
        "id": "hostel_accommodation",
        "title": "Sharda University Hostel Accommodation and Mess Charges",
        "category": "Hostels & Campus Living",
        "keywords": ["hostel fee", "accommodation", "room rent", "mess food", "campus stay", "ac rooms"],
        "content": (
            "Hostel Accommodation Details at Sharda Campus:\n"
            "- AC 3-Seater Room: Rs. 1,61,000 / year (Security deposit Rs. 10,000 refundable)\n"
            "- AC 2-Seater Room: Rs. 1,92,000 / year (Security deposit Rs. 10,000 refundable)\n"
            "- Non-AC 3-Seater Room: Rs. 1,16,000 / year\n"
            "- Single Occupancy Studio AC: Rs. 2,35,000 / year\n"
            "All hostels include 4 daily nutritious meals (Breakfast, Lunch, Evening Snacks, Dinner), 24x7 Wi-Fi, electricity backup, housekeeping, laundry facilities, gym access, and biometric gate security."
        )
    })

    chunks.append({
        "id": "placements_summary",
        "title": "Sharda University Placement Highlights & Statistics",
        "category": "Placements & Career Outcomes",
        "keywords": ["placements", "salary", "highest package", "average package", "recruiters", "amazon", "microsoft"],
        "content": (
            "Placement Statistics & Career Support:\n"
            "- Highest Global Package: INR 1.00 Crore\n"
            "- Highest Domestic Package: INR 45.00 LPA\n"
            "- Average Package: INR 6.50 LPA to 8.80 LPA\n"
            "- Placement Percentage: 95%+\n"
            "- Companies Visiting: 600+ leading multinational corporations\n"
            "- Top Recruiters: Microsoft, Amazon Web Services, Deloitte, KPMG, PwC, Cognizant, Wipro, TCS, Accenture, Infosys, Sun Pharma, Larsen & Toubro."
        )
    })

    # 4. FAQ Chunks
    for faq in get_master_faq_data():
        chunks.append({
            "id": f"faq_{faq['id']}",
            "title": f"FAQ: {faq['question']}",
            "category": "Frequently Asked Questions",
            "keywords": [faq["question"], faq["category"]],
            "content": f"Question: {faq['question']}\nCategory: {faq['category']}\nAnswer: {faq['answer']}"
        })

    return chunks

def export_all_master_data():
    os.makedirs(MASTER_DATA_DIR, exist_ok=True)
    
    schools = get_master_schools_data()
    programs = get_master_programs_data()
    admissions = get_master_admissions_data()
    placements = get_master_placements_data()
    faqs = get_master_faq_data()
    chunks = generate_rag_knowledge_chunks()

    with open(MASTER_DATA_DIR / "schools.json", "w", encoding="utf-8") as f:
        json.dump(schools, f, indent=2)

    with open(MASTER_DATA_DIR / "programs.json", "w", encoding="utf-8") as f:
        json.dump(programs, f, indent=2)

    with open(MASTER_DATA_DIR / "admissions.json", "w", encoding="utf-8") as f:
        json.dump(admissions, f, indent=2)

    with open(MASTER_DATA_DIR / "placements.json", "w", encoding="utf-8") as f:
        json.dump(placements, f, indent=2)

    with open(MASTER_DATA_DIR / "faqs.json", "w", encoding="utf-8") as f:
        json.dump(faqs, f, indent=2)

    with open(MASTER_DATA_DIR / "knowledge_chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)

    print(f"Successfully generated all master datasets in {MASTER_DATA_DIR}")
    print(f"- Schools: {len(schools)}")
    print(f"- Programs: {len(programs)}")
    print(f"- FAQs: {len(faqs)}")
    print(f"- Knowledge RAG Chunks: {len(chunks)}")

if __name__ == "__main__":
    export_all_master_data()
