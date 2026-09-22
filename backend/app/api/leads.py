from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from ..services.crm_service import crm_service

router = APIRouter(prefix="/leads", tags=["CRM & Lead Intelligence"])

class LeadCaptureRequest(BaseModel):
    full_name: str = Field(..., description="Candidate or Parent Name")
    email: Optional[str] = Field(None, description="Email Address")
    phone: Optional[str] = Field(None, description="Contact Mobile Number")
    city: Optional[str] = "Delhi NCR"
    state: Optional[str] = "Uttar Pradesh"
    interested_school: Optional[str] = "General"
    interested_course: Optional[str] = "B.Tech CSE"
    source: Optional[str] = "website_rebuild"
    notes: Optional[str] = None
    utm_source: Optional[str] = "direct"
    utm_medium: Optional[str] = "organic"
    utm_campaign: Optional[str] = "sharda_2026_admission"
    chat_transcript: Optional[str] = None

class LeadStatusUpdateRequest(BaseModel):
    status: str = Field(..., description="NEW, CONTACTED, COUNSELING, ADMITTED, CLOSED")
    notes: Optional[str] = None

@router.post("/capture")
def capture_inquiry_lead(lead: LeadCaptureRequest):
    if not lead.phone and not lead.email:
        raise HTTPException(status_code=400, detail="At least Phone or Email is required to register an admission inquiry.")
    result = crm_service.save_lead(lead.model_dump())
    return result

@router.get("")
@router.get("/")
@router.get("/list")
def list_leads(
    status: Optional[str] = Query(None, description="Filter by status (NEW, CONTACTED, etc.)"),
    priority: Optional[str] = Query(None, description="Filter by priority (HOT, WARM, COLD)"),
    search: Optional[str] = Query(None, description="Search keyword across name/email/phone/course"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0)
):
    return crm_service.list_leads(status=status, priority=priority, search=search, limit=limit, offset=offset)

@router.patch("/{lead_id}/status")
def update_lead_status(lead_id: str, body: LeadStatusUpdateRequest):
    success = crm_service.update_lead_status(lead_id, body.status, body.notes)
    if not success:
        raise HTTPException(status_code=404, detail=f"Lead with ID {lead_id} not found.")
    return {"status": "updated", "lead_id": lead_id, "new_status": body.status}

@router.get("/analytics")
def get_lead_analytics():
    return crm_service.get_lead_analytics()

@router.get("/export/csv")
def export_leads_csv():
    csv_data = crm_service.export_leads_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=sharda_leads_export.csv"}
    )
