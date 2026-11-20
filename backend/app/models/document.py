import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    filename = Column(String, nullable=False)
    file_type = Column(String, default="PDF")  # PDF, DOC, TXT
    file_size_bytes = Column(Integer, default=0)
    page_count = Column(Integer, default=1)
    status = Column(String, default="Processing")  # Reviewed, Processing, Risk Found
    doc_type = Column(String, default="Commercial Contract")
    classification_confidence = Column(Float, default=0.95)
    raw_text = Column(Text, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Parties & Metadata JSON
    parties_json = Column(Text, default="[]")  # List of identified parties
    effective_date = Column(String, default="Undated")
    governing_law = Column(String, default="Indian Law")
    jurisdiction = Column(String, default="New Delhi / Mumbai")
    
    # Relationships
    clauses = relationship("Clause", back_populates="document", cascade="all, delete-orphan")
    risks = relationship("Risk", back_populates="document", cascade="all, delete-orphan")
    obligations = relationship("Obligation", back_populates="document", cascade="all, delete-orphan")
    compliance_checks = relationship("ComplianceCheck", back_populates="document", cascade="all, delete-orphan")
