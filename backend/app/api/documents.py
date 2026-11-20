import os
import shutil
import json
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from ..core.config import settings
from ..core.database import get_db
from ..models.document import Document
from ..models.analysis import Clause, Risk, Obligation, ComplianceCheck
from ..schemas.document import DocumentListItem, DocumentDetail, ClauseResponse
from ..services.extractor import extract_text_with_pages, segment_clauses
from ..services.classifier import classify_document
from ..services.ner_extractor import extract_legal_entities
from ..services.risk_analyzer import analyze_clause_risks
from ..services.obligation_engine import extract_obligations
from ..services.compliance_engine import audit_compliance

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("", response_model=List[DocumentListItem])
def list_documents(db: Session = Depends(get_db)):
    """List all analyzed documents with status and metadata matching reference dashboard."""
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    results = []
    for d in docs:
        risk_count = db.query(Risk).filter(Risk.document_id == d.id).count()
        results.append(DocumentListItem(
            id=d.id,
            title=d.title,
            filename=d.filename,
            file_type=d.file_type,
            page_count=d.page_count,
            status=d.status,
            doc_type=d.doc_type,
            classification_confidence=d.classification_confidence,
            uploaded_at=d.uploaded_at,
            clauses_flagged=risk_count
        ))
    return results

@router.get("/{doc_id}", response_model=DocumentDetail)
def get_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.get("/{doc_id}/clauses", response_model=List[ClauseResponse])
def get_document_clauses(doc_id: int, db: Session = Depends(get_db)):
    clauses = db.query(Clause).filter(Clause.document_id == doc_id).order_by(Clause.order_index).all()
    return clauses

@router.post("/upload", response_model=DocumentDetail)
async def upload_document(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Ingest PDF, DOCX, or TXT file, parse pages, segment clauses, classify, and run full intelligence pipeline.
    """
    safe_filename = file.filename.replace(" ", "_")
    dest_path = settings.UPLOAD_DIR / safe_filename
    
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = dest_path.stat().st_size
    ext = dest_path.suffix.upper().replace(".", "")
    doc_title = title if title and title.strip() else file.filename.replace(".pdf", "").replace(".docx", "").replace(".txt", "")

    # 1. Extract text preserving pages
    pages_data = extract_text_with_pages(dest_path)
    page_count = len(pages_data)
    full_text = "\n\n".join([p["text"] for p in pages_data])

    # 2. Segment clauses
    segmented = segment_clauses(pages_data)

    # 3. Classify Document Type
    doc_type, conf = classify_document(full_text)

    # 4. Extract Legal Entities
    entities = extract_legal_entities(full_text)

    # 5. Analyze Risks
    risks = analyze_clause_risks(segmented)

    # 6. Extract Obligations
    obligations = extract_obligations(segmented)

    # 7. Audit Compliance
    compliance_items = audit_compliance(full_text, doc_type)

    # Determine status: "Risk Found" if any High/Critical risk, else "Reviewed"
    has_high_risk = any(r["severity"] in ["Critical", "High"] for r in risks)
    doc_status = "Risk Found" if has_high_risk else "Reviewed"

    # Create Document record
    new_doc = Document(
        title=doc_title,
        filename=file.filename,
        file_type=ext if ext in ["PDF", "DOC", "DOCX", "TXT"] else "PDF",
        file_size_bytes=file_size,
        page_count=page_count,
        status=doc_status,
        doc_type=doc_type,
        classification_confidence=conf,
        raw_text=full_text,
        parties_json=json.dumps(entities.get("parties", [])),
        effective_date=entities.get("effective_date", "Undated"),
        governing_law=entities.get("governing_law", "Indian Law"),
        jurisdiction=entities.get("jurisdiction", "New Delhi, India")
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Save Clauses
    clause_orm_list = []
    for c in segmented:
        clause_orm = Clause(
            document_id=new_doc.id,
            clause_number=c["clause_number"],
            heading=c["heading"],
            text=c["text"],
            page_number=c["page_number"],
            order_index=c["order_index"]
        )
        db.add(clause_orm)
        clause_orm_list.append(clause_orm)
    db.commit()

    # Save Risks
    for r in risks:
        risk_orm = Risk(
            document_id=new_doc.id,
            title=r["title"],
            category=r["category"],
            severity=r["severity"],
            confidence=r["confidence"],
            explanation=r["explanation"],
            remediation=r["remediation"],
            clause_reference=r["clause_reference"],
            page_number=r["page_number"]
        )
        db.add(risk_orm)

    # Save Obligations
    for o in obligations:
        ob_orm = Obligation(
            document_id=new_doc.id,
            responsible_party=o["responsible_party"],
            action=o["action"],
            deadline_text=o["deadline_text"],
            due_date=o.get("due_date"),
            amount=o["amount"],
            category=o["category"],
            is_ambiguous=o["is_ambiguous"],
            clause_reference=o["clause_reference"],
            page_number=o["page_number"]
        )
        db.add(ob_orm)

    # Save Compliance
    for comp in compliance_items:
        comp_orm = ComplianceCheck(
            document_id=new_doc.id,
            statute_name=comp["statute_name"],
            section_reference=comp["section_reference"],
            requirement=comp["requirement"],
            status=comp["status"],
            details=comp["details"],
            source_url=comp["source_url"]
        )
        db.add(comp_orm)

    db.commit()
    db.refresh(new_doc)
    return new_doc

@router.delete("/{doc_id}")
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "Document deleted successfully"}
