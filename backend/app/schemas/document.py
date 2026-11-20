from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

class ClauseBase(BaseModel):
    clause_number: str
    heading: str
    text: str
    page_number: int = 1
    order_index: int = 0

class ClauseResponse(ClauseBase):
    id: int
    document_id: int

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str
    filename: str
    file_type: str = "PDF"
    doc_type: str = "Commercial Contract"

class DocumentListItem(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    page_count: int
    status: str
    doc_type: str
    classification_confidence: float
    uploaded_at: datetime
    clauses_flagged: int = 0

    class Config:
        from_attributes = True

class DocumentDetail(BaseModel):
    id: int
    title: str
    filename: str
    file_type: str
    file_size_bytes: int
    page_count: int
    status: str
    doc_type: str
    classification_confidence: float
    uploaded_at: datetime
    parties_json: str
    effective_date: str
    governing_law: str
    jurisdiction: str
    raw_text: str

    class Config:
        from_attributes = True
