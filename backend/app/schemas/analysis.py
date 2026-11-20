from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class RiskResponse(BaseModel):
    id: int
    document_id: int
    title: str
    category: str
    severity: str
    confidence: float
    explanation: str
    remediation: str
    clause_reference: str
    page_number: int
    user_feedback: Optional[str] = None

    class Config:
        from_attributes = True

class RiskFeedbackRequest(BaseModel):
    risk_id: int
    feedback: str  # "agree", "disagree", "reviewed"

class ObligationResponse(BaseModel):
    id: int
    document_id: int
    responsible_party: str
    action: str
    deadline_text: str
    due_date: Optional[datetime] = None
    amount: str
    category: str
    is_ambiguous: bool
    clause_reference: str
    page_number: int

    class Config:
        from_attributes = True

class ComplianceResponse(BaseModel):
    id: int
    document_id: int
    statute_name: str
    section_reference: str
    requirement: str
    status: str
    details: str
    source_url: str

    class Config:
        from_attributes = True

class ComparisonRequest(BaseModel):
    doc1_id: int
    doc2_id: int

class ClauseDiffItem(BaseModel):
    change_type: str  # "MODIFIED", "ADDED", "REMOVED", "IDENTICAL"
    clause_title: str
    doc1_text: Optional[str] = None
    doc2_text: Optional[str] = None
    doc1_clause_ref: Optional[str] = None
    doc2_clause_ref: Optional[str] = None
    impact_explanation: str
    is_contradiction: bool = False

class ComparisonResponse(BaseModel):
    doc1_title: str
    doc2_title: str
    total_modifications: int
    contradictions_count: int
    diff_items: List[ClauseDiffItem]
    summary: str

class QARequest(BaseModel):
    document_id: int
    question: str
    language: str = "en"  # "en", "hi", "pa"

class QAResponse(BaseModel):
    answer: str
    language: str
    confidence: float
    clause_citations: List[str]
    page_references: List[int]
    evidence_text: str

class SimplificationRequest(BaseModel):
    text: str
    language: str = "en"  # "en", "hi", "pa"

class SimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str
    language: str
    readability_gain: float
