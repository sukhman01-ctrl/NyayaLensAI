from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.document import Document
from ..models.analysis import Risk, Obligation, ComplianceCheck
from ..services.report_generator import generate_pdf_report, generate_markdown_report

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/pdf/{doc_id}")
def download_pdf_report(doc_id: int, db: Session = Depends(get_db)):
    """Generate and download formatted PDF audit report."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    risks = [r.__dict__ for r in db.query(Risk).filter(Risk.document_id == doc.id).all()]
    obligations = [o.__dict__ for o in db.query(Obligation).filter(Obligation.document_id == doc.id).all()]
    compliance = [c.__dict__ for c in db.query(ComplianceCheck).filter(ComplianceCheck.document_id == doc.id).all()]

    pdf_bytes = generate_pdf_report(doc.__dict__, risks, obligations, compliance)
    
    filename = f"NyayaLens_Report_{doc.title.replace(' ', '_')}.pdf"
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/markdown/{doc_id}", response_class=PlainTextResponse)
def download_markdown_report(doc_id: int, db: Session = Depends(get_db)):
    """Generate and download comprehensive Markdown legal dossier."""
    doc = db.query(Document).filter(Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    risks = [r.__dict__ for r in db.query(Risk).filter(Risk.document_id == doc.id).all()]
    obligations = [o.__dict__ for o in db.query(Obligation).filter(Obligation.document_id == doc.id).all()]
    compliance = [c.__dict__ for c in db.query(ComplianceCheck).filter(ComplianceCheck.document_id == doc.id).all()]

    md_content = generate_markdown_report(doc.__dict__, risks, obligations, compliance)
    return md_content
