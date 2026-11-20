from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.analysis import Obligation
from ..schemas.analysis import ObligationResponse

router = APIRouter(prefix="/obligations", tags=["Obligations & Deadlines"])

@router.get("/{doc_id}", response_model=List[ObligationResponse])
def get_document_obligations(doc_id: int, db: Session = Depends(get_db)):
    """Retrieve extracted obligations, responsible parties, and deadlines for timeline/calendar."""
    obligations = db.query(Obligation).filter(Obligation.document_id == doc_id).all()
    return obligations
