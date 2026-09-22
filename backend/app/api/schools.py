from fastapi import APIRouter, HTTPException
from typing import Optional
import json
from pathlib import Path

router = APIRouter(prefix="/schools", tags=["Schools & Departments"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MASTER_DATA_DIR = BASE_DIR / "scraper" / "output" / "master_data"

def get_schools():
    file_path = MASTER_DATA_DIR / "schools.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@router.get("/")
def list_schools():
    schools = get_schools()
    return {"total": len(schools), "data": schools}

@router.get("/{slug}")
def get_school_by_slug(slug: str):
    schools = get_schools()
    for s in schools:
        if s.get("slug") == slug or s.get("id") == slug:
            return s
    raise HTTPException(status_code=404, detail="School not found")
