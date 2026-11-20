import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class Clause(Base):
    __tablename__ = "clauses"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    clause_number = Column(String, default="Clause")
    heading = Column(String, default="General Clause")
    text = Column(Text, nullable=False)
    page_number = Column(Integer, default=1)
    order_index = Column(Integer, default=0)

    document = relationship("Document", back_populates="clauses")
    risks = relationship("Risk", back_populates="clause")


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    clause_id = Column(Integer, ForeignKey("clauses.id", ondelete="SET NULL"), nullable=True)
    
    title = Column(String, nullable=False)
    category = Column(String, default="Liability")  # Liability, Termination, Penalty, Confidentiality, Compliance, IP
    severity = Column(String, default="Medium")     # Critical, High, Medium, Low
    confidence = Column(Float, default=0.90)       # 0.0 - 1.0
    explanation = Column(Text, nullable=False)
    remediation = Column(Text, default="")
    clause_reference = Column(String, default="")
    page_number = Column(Integer, default=1)
    user_feedback = Column(String, nullable=True)   # agree, disagree, reviewed

    document = relationship("Document", back_populates="risks")
    clause = relationship("Clause", back_populates="risks")


class Obligation(Base):
    __tablename__ = "obligations"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    responsible_party = Column(String, default="Party")
    action = Column(Text, nullable=False)
    deadline_text = Column(String, default="As specified")
    due_date = Column(DateTime, nullable=True)
    amount = Column(String, default="N/A")
    category = Column(String, default="Payment")    # Payment, Notice, Reporting, Delivery, Renewal
    is_ambiguous = Column(Boolean, default=False)
    clause_reference = Column(String, default="")
    page_number = Column(Integer, default=1)

    document = relationship("Document", back_populates="obligations")


class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False)
    
    statute_name = Column(String, nullable=False)
    section_reference = Column(String, default="")
    requirement = Column(Text, nullable=False)
    status = Column(String, default="Compliant")  # Compliant, Violation, Missing Clause, Insufficient Information
    details = Column(Text, nullable=False)
    source_url = Column(String, default="https://www.indiacode.nic.in")

    document = relationship("Document", back_populates="compliance_checks")
