import os
import gzip
import shutil
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from .core.config import settings

# Auto-decompress master knowledge database if running from compressed archive
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "sharda_pages.db"
GZ_PATH = DATA_DIR / "sharda_pages.db.gz"

if not DB_PATH.exists() and GZ_PATH.exists():
    try:
        print("Decompressing master Sharda knowledge database (sharda_pages.db.gz)...")
        with gzip.open(GZ_PATH, "rb") as f_in:
            with open(DB_PATH, "wb") as f_out:
                shutil.copyfileobj(f_in, f_out)
        print("Database ready!")
    except Exception as e:
        print(f"Error decompressing database: {e}")

from .api import programs, schools, admissions, leads, ai, pages, replica, audit, cms, search

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Modern Headless Backend & Gemini RAG AI Platform for Sharda University"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enterprise Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Route Registry
app.include_router(programs.router, prefix=settings.API_V1_STR)
app.include_router(schools.router, prefix=settings.API_V1_STR)
app.include_router(admissions.router, prefix=settings.API_V1_STR)
app.include_router(leads.router, prefix=settings.API_V1_STR)
app.include_router(cms.router, prefix=settings.API_V1_STR)
app.include_router(audit.router, prefix=settings.API_V1_STR)
app.include_router(ai.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)
app.include_router(pages.router, prefix=settings.API_V1_STR)
app.include_router(replica.router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "service": "Sharda University Modern API"
    }

@app.get("/api")
def api_root():
    return {
        "message": "Welcome to Sharda University Modern API & AI Brain",
        "docs": "/docs",
        "endpoints": {
            "replica": "/replica",
            "programs": f"{settings.API_V1_STR}/programs",
            "schools": f"{settings.API_V1_STR}/schools",
            "admissions": f"{settings.API_V1_STR}/admissions",
            "pages": f"{settings.API_V1_STR}/pages/index",
            "ai_chat": f"{settings.API_V1_STR}/ai/chat",
            "leads": f"{settings.API_V1_STR}/leads/capture"
        }
    }
