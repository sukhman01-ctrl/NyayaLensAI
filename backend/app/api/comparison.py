from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.document import Document
from ..models.analysis import Clause
from ..schemas.analysis import ComparisonRequest, ComparisonResponse
from ..services.diff_engine import compare_documents

router = APIRouter(prefix="/comparison", tags=["Cross-Document Comparison"])

@router.post("", response_model=ComparisonResponse)
def compare_two_documents(comp_req: ComparisonRequest, db: Session = Depends(get_db)):
    """Compare two documents semantically and detect contradictions."""
    doc1 = db.query(Document).filter(Document.id == comp_req.doc1_id).first()
    doc2 = db.query(Document).filter(Document.id == comp_req.doc2_id).first()

    if not doc1 or not doc2:
        raise HTTPException(status_code=404, detail="One or both documents not found for comparison")

    clauses1 = db.query(Clause).filter(Clause.document_id == doc1.id).order_by(Clause.order_index).all()
    clauses2 = db.query(Clause).filter(Clause.document_id == doc2.id).order_by(Clause.order_index).all()

    c1_list = [{"clause_number": c.clause_number, "heading": c.heading, "text": c.text} for c in clauses1]
    c2_list = [{"clause_number": c.clause_number, "heading": c.heading, "text": c.text} for c in clauses2]

    res = compare_documents(c1_list, c2_list, doc1.title, doc2.title)
    return res
