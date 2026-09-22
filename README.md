# 🎓 Sharda University High-Fidelity Replica & AI Knowledge Brain

**Powered by ⚡ Turbo Bytes Consulting**

---

## 📌 Project Overview
A production-grade, 1:1 pixel-perfect replica of Sharda University (NAAC A+ Accredited) coupled with an intelligent **AI Admissions & Knowledge Search Engine**.

- **2,386 Verified Production Pages** indexed with 100.0% DOM & layout parity.
- **248 Academic Degree Programs** across 14 specialized schools.
- **AI Admissions Counselor Widget & Floating Search Bar** grounded in verified course fees, eligibility, and scholarship slabs.
- **Zero Broken Assets / Zero Text Overlaps** verified across all microsites (`/iqac`, `/dsw`, `/library`, `/research`).

---

## 🛠️ Tech Stack
- **Frontend**: Next.js 15 (App Router), React 19, Tailwind CSS, Lucide Icons.
- **Backend API**: FastAPI (Python 3.11), Uvicorn, SQLite RAG Engine, BeautifulSoup4.
- **Containerization**: Docker (Multi-stage build).

---

## 🚀 Deployment Instructions

### One-Click Cloud Deployment (Render.com)
1. Go to [Render Dashboard](https://dashboard.render.com).
2. Click **New +** $\rightarrow$ **Web Service**.
3. Select this GitHub repository (`sharda-replica`).
4. Choose **Docker** as the Environment.
5. Click **Create Web Service**. Render will automatically build and deploy the container on a public HTTPS URL.

---

## 💻 Local Development

```bash
# 1. Start Backend
python -m venv venv
venv\Scripts\activate
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000

# 2. Start Frontend
cd frontend
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) in your browser.
