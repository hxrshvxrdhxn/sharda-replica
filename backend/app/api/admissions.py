from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter(prefix="/admissions", tags=["Admissions & Scholarships"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
MASTER_DATA_DIR = BASE_DIR / "scraper" / "output" / "master_data"

def get_admissions_data():
    file_path = MASTER_DATA_DIR / "admissions.json"
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

@router.get("/")
def get_admission_details():
    return get_admissions_data()

@router.get("/scholarships")
def get_scholarships():
    data = get_admissions_data()
    return {"scholarships": data.get("scholarships", [])}

@router.get("/hostel-fees")
def get_hostel_fees():
    data = get_admissions_data()
    return {"hostel_fees": data.get("hostel_fees", [])}
