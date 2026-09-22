from fastapi import APIRouter, Query, HTTPException
from typing import Optional, List
import json
from pathlib import Path

router = APIRouter(prefix="/programs", tags=["Programs & Courses"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MASTER_DATA_DIR = BASE_DIR / "scraper" / "output" / "master_data"

def get_programs():
    file_path = MASTER_DATA_DIR / "programs.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("/")
def list_programs(
    school_id: Optional[str] = Query(None, description="Filter by school ID (e.g., set, sbs, smsr)"),
    degree: Optional[str] = Query(None, description="Filter by degree type (UG/PG)"),
    search: Optional[str] = Query(None, description="Search query")
):
    programs = get_programs()
    if school_id:
        programs = [p for p in programs if p.get("school_id") == school_id]
    if degree:
        programs = [p for p in programs if degree.lower() in p.get("degree", "").lower()]
    if search:
        s = search.lower()
        programs = [
            p for p in programs 
            if s in p.get("name", "").lower() 
            or any(s in spec.lower() for spec in p.get("specializations", []))
            or s in p.get("school", "").lower()
        ]
    return {"total": len(programs), "data": programs}

@router.get("/{slug}")
def get_program_by_slug(slug: str):
    programs = get_programs()
    for p in programs:
        if p.get("slug") == slug:
            return p
    raise HTTPException(status_code=404, detail="Program not found")
