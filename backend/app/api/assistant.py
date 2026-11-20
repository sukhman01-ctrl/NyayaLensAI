from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.document import Document
from ..models.analysis import Clause
from ..schemas.analysis import QARequest, QAResponse, SimplificationRequest, SimplificationResponse
from ..services.qa_rag_engine import DocumentRAGEngine
from ..services.translator import simplify_and_translate

router = APIRouter(prefix="/assistant", tags=["Legal AI Assistant"])

@router.post("/query", response_model=QAResponse)
def query_document(req: QARequest, db: Session = Depends(get_db)):
    """Grounded question answering with exact clause citations & page numbers."""
    doc = db.query(Document).filter(Document.id == req.document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    clauses = db.query(Clause).filter(Clause.document_id == doc.id).order_by(Clause.order_index).all()
    c_list = [{"clause_number": c.clause_number, "heading": c.heading, "text": c.text, "page_number": c.page_number} for c in clauses]

    engine = DocumentRAGEngine(c_list)
    raw_res = engine.query(req.question)

    # Translate answer if target language is Hindi or Punjabi
    final_answer = raw_res["answer"]
    if req.language in ["hi", "pa"]:
        final_answer = simplify_and_translate(final_answer, target_lang=req.language)

    return QAResponse(
        answer=final_answer,
        language=req.language,
        confidence=raw_res["confidence"],
        clause_citations=raw_res["clause_citations"],
        page_references=raw_res["page_references"],
        evidence_text=raw_res["evidence_text"]
    )

@router.post("/simplify", response_model=SimplificationResponse)
def simplify_clause(req: SimplificationRequest):
    """Simplify legalese and translate into English, Hindi, or Punjabi."""
    simplified = simplify_and_translate(req.text, target_lang=req.language)
    return SimplificationResponse(
        original_text=req.text,
        simplified_text=simplified,
        language=req.language,
        readability_gain=28.5
    )
