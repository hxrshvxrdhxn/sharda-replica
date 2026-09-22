from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from ..services.cms_service import cms_service

router = APIRouter(prefix="/cms", tags=["Headless CMS Engine"])

class BannerCreateRequest(BaseModel):
    title: str = Field(..., description="Banner Title")
    subtitle: Optional[str] = None
    image_url: str = Field(..., description="Image path or URL")
    cta_text: Optional[str] = "Apply Now"
    cta_link: Optional[str] = "/admissions"
    target_school: Optional[str] = "global"
    display_order: Optional[int] = 0

class AnnouncementCreateRequest(BaseModel):
    title: str = Field(..., description="Announcement text")
    category: Optional[str] = "Admissions"
    link_url: Optional[str] = "/admissions"
    is_urgent: Optional[bool] = False

@router.get("/banners")
def list_banners(school: Optional[str] = Query(None)):
    return cms_service.list_banners(school)

@router.post("/banners")
def create_banner(banner: BannerCreateRequest):
    banner_id = cms_service.create_banner(banner.model_dump())
    return {"status": "created", "banner_id": banner_id}

@router.delete("/banners/{banner_id}")
def delete_banner(banner_id: int):
    success = cms_service.delete_banner(banner_id)
    if not success:
        raise HTTPException(status_code=404, detail="Banner not found")
    return {"status": "deleted", "banner_id": banner_id}

@router.get("/announcements")
def list_announcements():
    return cms_service.list_announcements()

@router.post("/announcements")
def create_announcement(ann: AnnouncementCreateRequest):
    ann_id = cms_service.create_announcement(ann.model_dump())
    return {"status": "created", "announcement_id": ann_id}

@router.delete("/announcements/{ann_id}")
def delete_announcement(ann_id: int):
    success = cms_service.delete_announcement(ann_id)
    if not success:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return {"status": "deleted", "announcement_id": ann_id}
