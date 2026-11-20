from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.analysis import ComplianceCheck
from ..schemas.analysis import ComplianceResponse

router = APIRouter(prefix="/compliance", tags=["Compliance Checker"])

@router.get("/{doc_id}", response_model=List[ComplianceResponse])
def get_document_compliance(doc_id: int, db: Session = Depends(get_db)):
    """Retrieve Indian statutory compliance checks and missing clauses for a document."""
    items = db.query(ComplianceCheck).filter(ComplianceCheck.document_id == doc_id).all()
    return items
