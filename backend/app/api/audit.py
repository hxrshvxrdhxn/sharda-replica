import asyncio
from fastapi import APIRouter, BackgroundTasks, Query
from typing import Optional
from ..services.audit_service import audit_service

router = APIRouter(prefix="/audit", tags=["Automated Quality & Audit Engine"])

@router.post("/run")
async def trigger_audit(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = Query(None, description="Max URLs to audit"),
    category: Optional[str] = Query(None, description="Filter by category (e.g., schools, programmes, admissions)")
):
    if audit_service.is_running:
        return {"status": "in_progress", "progress": audit_service.progress}
    
    background_tasks.add_task(audit_service.run_full_audit, limit, category)
    return {
        "status": "started",
        "message": f"Audit triggered for category '{category or 'ALL'}' with limit {limit or 'ALL'}",
        "initial_progress": audit_service.progress
    }

@router.get("/status")
def get_audit_status():
    return audit_service.get_audit_summary()

@router.get("/report")
def get_audit_report():
    return audit_service.get_audit_summary()
