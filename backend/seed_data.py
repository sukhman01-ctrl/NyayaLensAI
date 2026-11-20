"""
Database Seeder for NyayaLens AI
Initializes realistic sample documents matching the user's reference dashboard.
"""

import os
import json
import datetime
# pyrefly: ignore[missing-import]
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.document import Document
from app.models.analysis import Clause, Risk, Obligation, ComplianceCheck
from app.models.user import User
# pyrefly: ignore[missing-import]
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

SAMPLE_DOCS = [
    {
        "title": "Master Service Agreement — TechCorp Inc.",
        "filename": "Master_Service_Agreement_TechCorp.pdf",
        "file_type": "PDF",
        "file_size_bytes": 1048576,
        "page_count": 47,
        "status": "Reviewed",
        "doc_type": "Master Service Agreement",
        "classification_confidence": 0.97,
        "parties": ["TechCorp Inc. (Client)", "DataStream Solutions Pvt. Ltd. (Provider)"],
        "effective_date": "15th January 2024",
        "governing_law": "Laws of the Republic of India",
        "jurisdiction": "Courts at New Delhi, India",
        "raw_text": """MASTER SERVICE AGREEMENT

This Master Service Agreement ("Agreement") is made and entered into as of 15th January 2024 ("Effective Date"), by and between TechCorp Inc., a corporation organized under the laws of Delaware having offices at New York, USA ("Client"), and DataStream Solutions Pvt. Ltd., a private limited company incorporated under the Companies Act, 2013 having its registered office at Cyber City, Gurugram, Haryana, India ("Service Provider").

Clause 1. Scope of Services
Service Provider shall provide enterprise cloud engineering, NLP pipeline maintenance, and technical consulting deliverables as described in individual Statements of Work ("SOW") executed hereunder.

Clause 2. Term and Mutual Renewal
This Agreement shall commence on the Effective Date and continue for an initial period of three (3) years. It shall automatically renew for successive one (1) year terms unless either party provides written notice of non-renewal at least sixty (60) days prior to the expiration of the then-current term.

Clause 3. Invoicing and Payment Terms
Client shall pay undisputed fees within thirty (30) days from the date of receipt of each valid tax invoice. All payments shall be made in INR or equivalent USD via electronic wire transfer. Failure to pay within forty-five (45) days shall incur statutory interest of 1.5% per month.

Clause 4. Confidentiality and Trade Secrets
Each party acknowledges that in connection with this Agreement, it may receive confidential and proprietary technical data. The Receiving Party shall protect such Confidential Information with the same degree of care it uses for its own proprietary information, but no less than reasonable care, for a period of five (5) years post-termination.

Clause 5. Termination for Convenience
Either party may terminate this Agreement or any SOW for convenience upon ninety (90) days prior written notice to the other party. In the event of material breach, the non-breaching party may terminate forthwith if such breach remains uncured for thirty (30) days following written notice.

Clause 8.3 Limitation of Liability
To the maximum extent permitted under applicable law, the aggregate liability of Service Provider arising out of or related to this Agreement or any SOW, whether in contract, tort, indemnity, or otherwise, shall not exceed the total fees actually received by Service Provider under the applicable SOW in the one (1) month preceding the incident, or $10,000, whichever is less. In no event shall either party be liable for any indirect, incidental, or consequential damages.

Clause 12. Intellectual Property Rights and Ownership
All Pre-Existing IP belonging to a party prior to the Effective Date shall remain the exclusive property of that party. Client shall own all right, title, and interest in and to the custom deliverables, source code, and reports created specifically for Client under this Agreement. Service Provider is granted a non-exclusive license to use generic frameworks and utilities developed independently.

Clause 14. Dispute Resolution and Governing Law
This Agreement shall be governed by and construed in accordance with the substantive laws of India. Any dispute or controversy arising out of or in connection with this contract shall be referred to and finally resolved by arbitration administered in New Delhi in accordance with the Arbitration and Conciliation Act, 1996. Courts at New Delhi shall have exclusive supervisory jurisdiction.
""",
        "risks": [
            {
                "title": "LIMITATION OF LIABILITY RISK",
                "category": "Liability",
                "severity": "Critical",
                "confidence": 0.94,
                "explanation": "Clause 8.3 caps liability at $10K (or 1 month fee) — significantly below industry standard for enterprise cloud services. Leaves client exposed to unrecoverable breach damages.",
                "remediation": "Recommend renegotiating liability cap to at least 12 months trailing fees or direct insurance coverage limits.",
                "clause_reference": "Clause 8.3",
                "page_number": 8
            },
            {
                "title": "TERMINATION NOTICE GAP",
                "category": "Termination",
                "severity": "Medium",
                "confidence": 0.88,
                "explanation": "Termination for convenience requires 90 days notice, which is manageable but may prolong unwanted vendor dependencies.",
                "remediation": "Ensure transitional handback milestones are explicitly enforceable during the 90-day window.",
                "clause_reference": "Clause 5",
                "page_number": 5
            }
        ],
        "obligations": [
            {
                "responsible_party": "Client",
                "action": "Remit undisputed invoice amount",
                "deadline_text": "Within 30 days of invoice date",
                "amount": "$45,000 / month",
                "category": "Payment",
                "is_ambiguous": False,
                "clause_reference": "Clause 3",
                "page_number": 3
            },
            {
                "responsible_party": "Service Provider",
                "action": "Deliver quarterly SLA uptime and cloud engineering milestones",
                "deadline_text": "Quarterly by the 15th of month",
                "amount": "N/A",
                "category": "Delivery",
                "is_ambiguous": False,
                "clause_reference": "Clause 1",
                "page_number": 1
            },
            {
                "responsible_party": "Both Parties",
                "action": "Provide non-renewal notice if desiring contract exit",
                "deadline_text": "60 days prior to contract expiry",
                "amount": "N/A",
                "category": "Renewal",
                "is_ambiguous": False,
                "clause_reference": "Clause 2",
                "page_number": 2
            }
        ],
        "compliance": [
            {
                "statute_name": "Indian Contract Act, 1872",
                "section_reference": "Section 73 (Compensation for Loss or Damage)",
                "requirement": "Breaching party is liable for natural loss; limitation caps must be equitable.",
                "status": "Compliant",
                "details": "Contractual cap is formally articulated, though commercially unfavorable.",
                "source_url": "https://www.indiacode.nic.in"
            },
            {
                "statute_name": "Arbitration and Conciliation Act, 1996",
                "section_reference": "Section 7 (Arbitration Agreement)",
                "requirement": "Written agreement specifying seat, rules, and appointing authority.",
                "status": "Compliant",
                "details": "Clause 14 validly references New Delhi seat under 1996 Act.",
                "source_url": "https://www.indiacode.nic.in"
            },
            {
                "statute_name": "Digital Personal Data Protection Act, 2023",
                "section_reference": "Section 6 (Data Fiduciary Safeguards)",
                "requirement": "Explicit data fiduciary obligations and security safeguards.",
                "status": "Missing Clause",
                "details": "No specialized data protection or breach notification clause found. DPDP compliance requires addendum.",
                "source_url": "https://www.meity.gov.in"
            }
        ]
    },
    {
        "title": "Employment Contract — Senior Engineer",
        "filename": "Employment_Contract_Senior_Engineer.doc",
        "file_type": "DOC",
        "file_size_bytes": 524288,
        "page_count": 18,
        "status": "Processing",
        "doc_type": "Employment Contract",
        "classification_confidence": 0.98,
        "parties": ["Apex Innovations Pvt. Ltd.", "Vikram Malhotra (Employee)"],
        "effective_date": "1st March 2024",
        "governing_law": "Laws of India",
        "jurisdiction": "Courts at Bengaluru, Karnataka",
        "raw_text": """EMPLOYMENT AGREEMENT

This Employment Agreement is entered into on 1st March 2024 between Apex Innovations Pvt. Ltd., having office at Bangalore, India, and Vikram Malhotra, residing at Indiranagar, Bangalore.

1. Position and Duties
The Employee is appointed as Principal AI Engineer and shall perform research and full-stack development duties with highest standard of diligence.

2. Remuneration and Benefits
The Company shall pay an annual gross salary of INR 32,00,000, payable in equal monthly installments subject to statutory TDS deductions and Provident Fund.

3. Probation and Termination Notice
The Employee shall be on probation for six (6) months. Either party may terminate employment by giving thirty (30) days written notice or payment of salary in lieu thereof.

4. Restrictive Covenants and Non-Compete
During employment and for a period of two (2) years following termination for any reason, Employee covenants that he shall not directly or indirectly engage with, consult for, or join any competing software firm operating in India or worldwide.
""",
        "risks": [
            {
                "title": "VOID NON-COMPETE COVENANT",
                "category": "Compliance",
                "severity": "Critical",
                "confidence": 0.98,
                "explanation": "Clause 4 imposes a 2-year post-employment non-compete. Under Section 27 of the Indian Contract Act, 1872, all post-termination restraint of trade agreements are void ab initio in India (Niranjan Shankar Golikari v. Century Spg & Mfg Co).",
                "remediation": "Delete post-termination non-compete. Retain only non-solicitation of clients and confidentiality protection.",
                "clause_reference": "Clause 4",
                "page_number": 4
            }
        ],
        "obligations": [
            {
                "responsible_party": "Employer",
                "action": "Disburse monthly remuneration and PF contribution",
                "deadline_text": "By 1st of each calendar month",
                "amount": "₹2,66,666 / month",
                "category": "Payment",
                "is_ambiguous": False,
                "clause_reference": "Clause 2",
                "page_number": 2
            }
        ],
        "compliance": [
            {
                "statute_name": "Indian Contract Act, 1872",
                "section_reference": "Section 27 (Agreement in Restraint of Trade)",
                "requirement": "Agreements restraining profession, trade, or business are void.",
                "status": "Violation",
                "details": "Post-employment non-compete violates Section 27.",
                "source_url": "https://www.indiacode.nic.in"
            }
        ]
    },
    {
        "title": "NDA — Global Partners LLC",
        "filename": "NDA_Global_Partners_LLC.pdf",
        "file_type": "PDF",
        "file_size_bytes": 262144,
        "page_count": 8,
        "status": "Risk Found",
        "doc_type": "Non-Disclosure Agreement",
        "classification_confidence": 0.96,
        "parties": ["Global Partners LLC", "InnoTech Ventures Pvt. Ltd."],
        "effective_date": "10th October 2024",
        "governing_law": "Laws of India",
        "jurisdiction": "Courts at Mumbai, Maharashtra",
        "raw_text": """MUTUAL NON-DISCLOSURE AGREEMENT

This Agreement is made as of 10th October 2024 between Global Partners LLC and InnoTech Ventures Pvt. Ltd.

1. Definition of Confidential Information
Includes all proprietary technical designs, trade secrets, financial projections, and client lists marked as confidential.

2. Non-Disclosure Obligations and Perpetual Term
Receiving Party agrees to protect Confidential Information in perpetuity. Any breach shall warrant immediate liquidated damages of USD $100,000 without requirement of proving actual loss.

3. Return of Materials
Upon request, Receiving Party shall forthwith destroy or return all confidential records.
""",
        "risks": [
            {
                "title": "LIQUIDATED DAMAGES PENALTY RISK",
                "category": "Penalty",
                "severity": "High",
                "confidence": 0.92,
                "explanation": "Automatic $100,000 liquidated damages clause without proof of actual loss may be struck down as an illegal penalty under Section 74 of the Indian Contract Act.",
                "remediation": "Modify to actual provable damages and injunctive relief.",
                "clause_reference": "Clause 2",
                "page_number": 2
            },
            {
                "title": "PERPETUAL CONFIDENTIALITY RISK",
                "category": "Confidentiality",
                "severity": "Medium",
                "confidence": 0.86,
                "explanation": "Perpetual duration for standard commercial data creates permanent liability exposure.",
                "remediation": "Cap duration at 3 to 5 years from disclosure date.",
                "clause_reference": "Clause 2",
                "page_number": 2
            }
        ],
        "obligations": [
            {
                "responsible_party": "Receiving Party",
                "action": "Return or destroy proprietary records upon demand",
                "deadline_text": "Promptly within 7 business days",
                "amount": "N/A",
                "category": "Delivery",
                "is_ambiguous": False,
                "clause_reference": "Clause 3",
                "page_number": 3
            }
        ],
        "compliance": [
            {
                "statute_name": "Indian Contract Act, 1872",
                "section_reference": "Section 74 (Compensation for Breach of Contract)",
                "requirement": "Liquidated damages must represent genuine reasonable compensation, not punishment.",
                "status": "Violation",
                "details": "Stipulated $100,000 fine exceeds reasonable pre-estimate.",
                "source_url": "https://www.indiacode.nic.in"
            }
        ]
    },
    {
        "title": "Licensing Agreement — SoftwareCo",
        "filename": "Licensing_Agreement_SoftwareCo.pdf",
        "file_type": "PDF",
        "file_size_bytes": 786432,
        "page_count": 32,
        "status": "Reviewed",
        "doc_type": "Commercial Contract",
        "classification_confidence": 0.95,
        "parties": ["SoftwareCo Technologies Ltd.", "Enterprise User Corp."],
        "effective_date": "20th November 2023",
        "governing_law": "Laws of India",
        "jurisdiction": "Courts at New Delhi, India",
        "raw_text": """SOFTWARE LICENSE AND SUBSCRIPTION AGREEMENT

Section 1. Grant of License
SoftwareCo grants Customer a non-exclusive, non-transferable, revocable subscription license to access the SaaS Platform.

Section 2. Fees and Invoicing
Subscription fees are billed annually in advance. Payments are due within thirty (30) days of receipt.

Section 12. Intellectual Property Rights
SoftwareCo retains all title, copyright, and patent rights in the SaaS platform and updates. No transfer of ownership occurs.

Section 15. Arbitration and Governing Law
Governed by the laws of India. Arbitration at New Delhi under the Arbitration and Conciliation Act, 1996.
""",
        "risks": [
            {
                "title": "IP OWNERSHIP CLEAR",
                "category": "IP",
                "severity": "Low",
                "confidence": 0.89,
                "explanation": "Intellectual property rights clearly defined in Section 12. No ambiguity detected.",
                "remediation": "Standard commercial terms.",
                "clause_reference": "Section 12",
                "page_number": 12
            }
        ],
        "obligations": [
            {
                "responsible_party": "Customer",
                "action": "Pay annual platform subscription license fee",
                "deadline_text": "Annually within 30 days of renewal",
                "amount": "₹12,00,000 / year",
                "category": "Payment",
                "is_ambiguous": False,
                "clause_reference": "Section 2",
                "page_number": 2
            }
        ],
        "compliance": [
            {
                "statute_name": "Indian Copyright Act, 1957",
                "section_reference": "Section 30 (Licenses by Owners of Copyright)",
                "requirement": "Written license specifying scope, territory, and duration.",
                "status": "Compliant",
                "details": "Software license conditions meet statutory criteria.",
                "source_url": "https://www.indiacode.nic.in"
            }
        ]
    },
    {
        "title": "Vendor Contract — DataStream Analytics",
        "filename": "Vendor_Contract_DataStream.doc",
        "file_type": "DOC",
        "file_size_bytes": 629145,
        "page_count": 24,
        "status": "Risk Found",
        "doc_type": "Commercial Contract",
        "classification_confidence": 0.94,
        "parties": ["DataStream Analytics Pvt. Ltd.", "Global Financial Systems Inc."],
        "effective_date": "5th January 2024",
        "governing_law": "Laws of India",
        "jurisdiction": "Courts at Hyderabad, Telangana",
        "raw_text": """VENDOR SERVICES CONTRACT

Clause 1. Data Analytics Deliverables
Vendor shall generate real-time predictive analytics models and data dashboards for Client operations.

Clause 7. Termination
Client may terminate forthwith at its sole discretion upon 15 days notice. Vendor must provide 60 days notice.

Clause 10. Indemnification and Consequential Damages
Vendor shall indemnify, defend and hold harmless Client from any and all claims, indirect damages, loss of profits, and business disruption.
""",
        "risks": [
            {
                "title": "UNCAPPED CONSEQUENTIAL INDEMNITY",
                "category": "Liability",
                "severity": "Critical",
                "confidence": 0.93,
                "explanation": "Clause 10 requires vendor to indemnify client against indirect and consequential damages (loss of profits, business disruption) with no financial cap.",
                "remediation": "Carve out indirect/consequential damages and establish liability ceiling.",
                "clause_reference": "Clause 10",
                "page_number": 10
            },
            {
                "title": "ASYMMETRIC TERMINATION NOTICE",
                "category": "Termination",
                "severity": "High",
                "confidence": 0.89,
                "explanation": "Client holds 15-day termination right while vendor is bound to 60 days.",
                "remediation": "Harmonize notice periods to mutual 30 or 60 days.",
                "clause_reference": "Clause 7",
                "page_number": 7
            }
        ],
        "obligations": [
            {
                "responsible_party": "Vendor",
                "action": "Maintain 99.9% uptime for data stream dashboards",
                "deadline_text": "Continuous monthly measurement",
                "amount": "N/A",
                "category": "Delivery",
                "is_ambiguous": False,
                "clause_reference": "Clause 1",
                "page_number": 1
            }
        ],
        "compliance": [
            {
                "statute_name": "Indian Contract Act, 1872",
                "section_reference": "Section 73 (Remoteness of Damage)",
                "requirement": "Compensation not given for remote or indirect loss under general statutory rule.",
                "status": "Violation",
                "details": "Contractual attempt to impose broad indirect loss indemnity.",
                "source_url": "https://www.indiacode.nic.in"
            }
        ]
    }
]

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Clear existing documents to seed cleanly
    db.query(ComplianceCheck).delete()
    db.query(Obligation).delete()
    db.query(Risk).delete()
    db.query(Clause).delete()
    db.query(Document).delete()
    db.commit()

    # Check or create default user
    admin_user = db.query(User).filter(User.email == "demo@nyayalens.ai").first()
    if not admin_user:
        admin_user = User(
            email="demo@nyayalens.ai",
            hashed_password=pwd_context.hash("demo123"),
            full_name="Senior Legal Counsel",
            role="Partner",
            is_active=True
        )
        db.add(admin_user)
        db.commit()

    print("[Seeder] Inserting sample documents matching reference UI...")

    for doc_item in SAMPLE_DOCS:
        new_doc = Document(
            title=doc_item["title"],
            filename=doc_item["filename"],
            file_type=doc_item["file_type"],
            file_size_bytes=doc_item["file_size_bytes"],
            page_count=doc_item["page_count"],
            status=doc_item["status"],
            doc_type=doc_item["doc_type"],
            classification_confidence=doc_item["classification_confidence"],
            raw_text=doc_item["raw_text"],
            parties_json=json.dumps(doc_item["parties"]),
            effective_date=doc_item["effective_date"],
            governing_law=doc_item["governing_law"],
            jurisdiction=doc_item["jurisdiction"],
            uploaded_at=datetime.datetime.utcnow() - datetime.timedelta(hours=int(doc_item["page_count"] // 5))
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)

        # Break text into clauses
        paragraphs = [p.strip() for p in doc_item["raw_text"].split("\n\n") if p.strip()]
        for idx, p in enumerate(paragraphs):
            lines = p.split("\n")
            first_line = lines[0].strip()
            heading = first_line[:50] if len(first_line) < 50 else f"Section {idx+1}"
            clause_num = f"Clause {idx+1}"
            if "clause" in first_line.lower() or "section" in first_line.lower():
                clause_num = first_line.split(":")[0].split(".")[0].strip()

            c_orm = Clause(
                document_id=new_doc.id,
                clause_number=clause_num,
                heading=heading,
                text=p,
                page_number=max(1, (idx // 2) + 1),
                order_index=idx
            )
            db.add(c_orm)

        # Add Risks
        for r in doc_item.get("risks", []):
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

        # Add Obligations
        for o in doc_item.get("obligations", []):
            ob_orm = Obligation(
                document_id=new_doc.id,
                responsible_party=o["responsible_party"],
                action=o["action"],
                deadline_text=o["deadline_text"],
                due_date=datetime.datetime.utcnow() + datetime.timedelta(days=30),
                amount=o["amount"],
                category=o["category"],
                is_ambiguous=o["is_ambiguous"],
                clause_reference=o["clause_reference"],
                page_number=o["page_number"]
            )
            db.add(ob_orm)

        # Add Compliance
        for c in doc_item.get("compliance", []):
            comp_orm = ComplianceCheck(
                document_id=new_doc.id,
                statute_name=c["statute_name"],
                section_reference=c["section_reference"],
                requirement=c["requirement"],
                status=c["status"],
                details=c["details"],
                source_url=c["source_url"]
            )
            db.add(comp_orm)

        db.commit()

    print("[Seeder] Successfully seeded database with all documents, clauses, risks, and compliance checks!")
    db.close()

if __name__ == "__main__":
    seed_database()
