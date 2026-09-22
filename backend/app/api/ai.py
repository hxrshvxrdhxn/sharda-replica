from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from ..services.rag_service import rag_service

router = APIRouter(prefix="/ai", tags=["Turbo Bytes Sharda AI (SAI) Brain Engine"])

class AIChatRequest(BaseModel):
    query: str = Field(..., example="What is the fee and eligibility for B.Tech Computer Science?")
    conversation_history: Optional[List[Dict[str, str]]] = Field(default_factory=list)

class AISearchRequest(BaseModel):
    query: str = Field(..., example="MBA scholarships")
    limit: Optional[int] = Field(5, ge=1, le=20)

@router.post("/chat")
async def chat_with_sharda_ai(req: AIChatRequest):
    result = await rag_service.generate_response(req.query, req.conversation_history)
    return {
        "success": True,
        "query": req.query,
        "answer": result["response"],
        "sources": result.get("sources", []),
        "matched_programs": result.get("matched_programs", []),
        "lead_capture_recommended": result.get("lead_capture_recommended", False),
        "model": result.get("model", "Turbo Bytes Grounded Brain Engine"),
        "powered_by": "Turbo Bytes Consulting"
    }

@router.get("/suggest")
@router.get("/autocomplete")
def suggest_programs(q: str = Query(..., description="Search query string"), limit: int = Query(6, ge=1, le=20)):
    matches = rag_service.search_programs(q, limit=limit)
    return {
        "success": True,
        "query": q,
        "total": len(matches),
        "suggestions": matches,
        "powered_by": "Turbo Bytes Consulting"
    }

@router.get("/search")
@router.post("/search")
async def search_sharda_knowledge(q: Optional[str] = None, req: Optional[AISearchRequest] = None):
    query = q or (req.query if req else "")
    limit = req.limit if req else 6
    matched_programs = rag_service.search_programs(query, limit=limit)
    chunks = rag_service.search_knowledge(query, top_k=limit)
    return {
        "success": True,
        "query": query,
        "total_programs": len(matched_programs),
        "programs": matched_programs,
        "total_knowledge_chunks": len(chunks),
        "knowledge_chunks": chunks,
        "powered_by": "Turbo Bytes Consulting"
    }

@router.post("/refresh-knowledge")
def refresh_knowledge():
    rag_service.load_knowledge()
    return {
        "success": True,
        "total_chunks": len(rag_service.knowledge_chunks),
        "total_programs": len(rag_service.programs_index),
        "total_pages": len(rag_service.page_index),
        "powered_by": "Turbo Bytes Consulting"
    }
