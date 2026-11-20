from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.analysis import Risk
from ..schemas.analysis import RiskResponse, RiskFeedbackRequest

router = APIRouter(prefix="/analysis", tags=["Risk Analysis"])

@router.get("/risks/{doc_id}", response_model=List[RiskResponse])
def get_document_risks(doc_id: int, db: Session = Depends(get_db)):
    """Retrieve all flagged risks for a given document."""
    risks = db.query(Risk).filter(Risk.document_id == doc_id).all()
    return risks

@router.post("/risk-feedback")
def submit_risk_feedback(feedback_data: RiskFeedbackRequest, db: Session = Depends(get_db)):
    """Store user evaluation feedback (agree, disagree, reviewed) for model calibration."""
    risk = db.query(Risk).filter(Risk.id == feedback_data.risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk record not found")
    risk.user_feedback = feedback_data.feedback
    db.commit()
    return {"message": "Feedback recorded successfully", "risk_id": risk.id, "status": feedback_data.feedback}
