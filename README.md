# ⚖️ NyayaLens AI – Intelligent Legal Document Understanding, Risk Detection and Decision Support System

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI%200.100+-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React%2018%20%2B%20Vite-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![TailwindCSS](https://img.shields.io/badge/UI-Tailwind%20CSS%203.4-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com)
[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?style=flat&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

An explainable, production-style legal document intelligence platform engineered specifically for Indian contracts, commercial leases, employment agreements, court orders, and legal notices. 

Going far beyond conventional summarisation, **NyayaLens AI** performs granular clause segmentation, detects high-liability risks with remediation counter-clauses, tracks deadlines in chronological timelines, compares multiple drafts for contradictions, checks compliance against verified Indian statutes (*Indian Contract Act 1872*, *Arbitration Act 1996*, *DPDP Act 2023*, *Stamp Act 1899*), and provides source-grounded multilingual explanations in **English**, **Hindi (हिन्दी)**, and **Punjabi (ਪੰਜਾਬੀ)**.

---

## 🎨 UI/UX Design Aesthetic

Styled after modern legal intelligence platforms (LexAI, Harvey, Ironclad, Robin AI):
- **Theme**: Deep Dark Luxury Navy (`#0B0F19` background, `#121929` elevated cards, thin translucent borders).
- **Status Pills**: 
  - `Reviewed`: Emerald green pill with dark backing
  - `Processing`: Blue/indigo glowing pill
  - `Risk Found`: Amber/orange warning pill
  - `Critical`: Crimson/red alert badge
- **Confidence Meters**: High-contrast purple gradient progress bars with exact percentage confidence scores ($94\%$, $98\%$, $89\%$, $91\%$).
- **Two-Panel Document Inspector**:
  - **Left Panel**: Original document structure with page markers and risk highlights.
  - **Right Panel**: Multi-tabbed intelligence suite (*Clause Risks*, *Obligations*, *Statutory Compliance*, *Metadata*, *Document QA Chat*).

---

## 🏛️ Six Core Functional Modules

### 1. Smart Legal Document Understanding
- Ingests **PDF, DOCX, and TXT** documents while preserving page numbers, clause hierarchies, and headings.
- Document Type Classifier (*Master Service Agreement, Employment Contract, Non-Disclosure Agreement, Residential Tenancy / Lease, Legal Notice, Court Judgment*).
- Named Entity Recognition (NER) for Parties, Execution Dates, Effective Dates, Governing Laws, and Jurisdictional Forums.
- Dual-panel synchronized document viewer.

### 2. Clause-Level Legal Risk Detection
- Categorizes risks into **Critical, High, Medium, and Low** severity.
- Detects asymmetric termination, nominal liability caps, overbroad consequential indemnity, illegal post-employment non-compete clauses, and punitive liquidated damages.
- Provides explainable legal hazard rationale, exact clause numbers, page numbers, and actionable remediation counter-clauses.
- Includes a user feedback mechanism (`Agree` / `Disagree`) to calibrate model accuracy.

### 3. Legal Obligation & Deadline Extractor
- Dissects contracts into actionable commitments: *Responsible Party*, *Action Required*, *Amount*, *Deadline*, and *Trigger Conditions*.
- Identifies payment schedules, renewal notification windows, milestone deliveries, and compliance reporting.
- Distinguishes strict deadlines from ambiguous terms (e.g. *"promptly"*, *"forthwith"*, *"within a reasonable time"*).

### 4. Cross-Document Comparison & Contradiction Detection
- Semantically aligns clauses between two drafts (e.g. Master Agreement vs Amendment, Principal Lease vs Addendum).
- Identifies **Added, Removed, and Modified** clauses.
- Automatically flags substantive **Contradictions** in payment figures, notice windows (e.g. 30 days vs 90 days), and altered liability covenants with practical legal impact explanations.

### 5. Legal Compliance & Missing Clause Analyzer
- Audits documents against a curated Indian Statutory Knowledge Base:
  - **Indian Contract Act, 1872**: Section 27 (Restraint of Trade / Non-Compete), Section 28 (Legal Recourse), Section 73 & 74 (Liquidated Damages).
  - **Arbitration & Conciliation Act, 1996**: Section 7 (Written Arbitration Agreement & Seat).
  - **Digital Personal Data Protection (DPDP) Act, 2023**: Data fiduciary duties & breach notification.
  - **Indian Stamp Act, 1899**: Section 35 (Stamping and court admissibility).
- Alerts users to missing essential clauses (Severability, Data Protection, Dispute Resolution).

### 6. Evidence-Backed Legal Explanation & Report Generation
- Simplifies complex legalese into layman's terms with authentic translations in **English**, **Hindi (हिन्दी)**, and **Punjabi (ਪੰਜਾਬੀ)**.
- Document-grounded conversational QA interface citing exact page numbers and clauses.
- Generates downloadable **PDF Audit Reports** and **Markdown Dossiers**.
- Prominently embeds formal informational disclaimers.

---

## 🏗️ Repository Architecture

```
NLPPROJECT/
│
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point & CORS
│   │   ├── core/                    # Config & Database sessions
│   │   ├── models/                  # SQLAlchemy ORM (Document, Clause, Risk, Obligation, Compliance)
│   │   ├── schemas/                 # Pydantic validation schemas
│   │   ├── api/                     # REST API routers (/documents, /analysis, /obligations, /comparison, /compliance, /assistant, /reports, /analytics)
│   │   └── services/
│   │       ├── extractor.py         # PDF/DOCX/TXT extractor with page mapping
│   │       ├── classifier.py        # TF-IDF Document Classifier
│   │       ├── ner_extractor.py     # Entity and metadata extractor
│   │       ├── risk_analyzer.py     # Clause risk scoring & explainability
│   │       ├── obligation_engine.py # Obligation and deadline extractor
│   │       ├── diff_engine.py       # Cross-document semantic diff & contradiction finder
│   │       ├── compliance_engine.py # Indian statutory compliance checker
│   │       ├── qa_rag_engine.py     # Grounded retrieval-augmented generation
│   │       ├── translator.py        # Multilingual English, Hindi, Punjabi engine
│   │       └── report_generator.py  # PDF and Markdown export
│   ├── seed_data.py                 # Initial database seeder
│   ├── run_backend.py               # Backend startup script
│   └── requirements.txt             # Backend dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Sidebar.tsx          # LexAI navigation bar
│   │   │   ├── Header.tsx           # Search, AI status pill, language dropdown
│   │   │   ├── MetricCards.tsx      # 4 KPI metrics cards
│   │   │   ├── RecentDocuments.tsx  # Document list with status pills
│   │   │   ├── AiInsightsStream.tsx # Stream cards with purple confidence meters
│   │   │   ├── DocumentWorkspace.tsx# Two-panel interactive workspace
│   │   │   ├── UploadModal.tsx      # Multi-format document upload
│   │   │   └── ComparisonModal.tsx  # Cross-document diff modal
│   │   ├── services/api.ts          # Frontend API service
│   │   ├── types/index.ts           # TypeScript interfaces
│   │   ├── App.tsx                  # Main layout
│   │   └── index.css                # Dark theme & styling
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- **Python 3.10+** (Python 3.12 verified)
- **Node.js 18+** & **npm**

### 2. Backend Setup & Startup
In your terminal:
```bash
# Navigate to backend
cd backend

# Install dependencies
py -m pip install -r requirements.txt

# Seed database with initial realistic sample documents
py seed_data.py

# Run FastAPI backend server (Port 8000)
py run_backend.py
```
> API Interactive Docs: **`http://127.0.0.1:8000/docs`**

### 3. Frontend Setup & Startup
In a second terminal:
```bash
# Navigate to frontend
cd frontend

# Install npm dependencies
npm install

# Start Vite React development server (Port 5173)
npm run dev
```
> Open your browser at **`http://127.0.0.1:5173`** to access the complete platform!

---

## 🎓 Academic Viva & Project Defense Guide

### Q1: How does NyayaLens AI detect clause risks without relying blindly on an external LLM API?
> **Answer:** NyayaLens AI uses a hybrid, explainable architecture. It employs rule-based pattern matching and lexical feature extraction against curated legal indicators for hazardous conditions (e.g. nominal liability caps, unilateral termination, uncapped indemnity). This ensures **deterministic, transparent, and reproducible** risk categorization without hallucinations or recurring API costs.

### Q2: Why is post-employment non-compete flagged as a Critical Risk under Indian Law?
> **Answer:** Under **Section 27 of the Indian Contract Act, 1872**, any agreement by which anyone is restrained from exercising a lawful profession, trade, or business of any kind is to that extent **void ab initio**. The Supreme Court of India in *Niranjan Shankar Golikari v. Century Spg & Mfg Co* affirmed that post-service restrictive covenants are strictly unenforceable in India.

### Q3: How is Cross-Document Contradiction Detection implemented?
> **Answer:** The engine segments both documents into clauses, computes a joint TF-IDF n-gram vector matrix, and evaluates cosine similarity to align related clauses. It then executes specialized entity difference checks across numerical monetary figures and notice period days. When terms diverge significantly (e.g. 30 days vs 90 days notice), it flags a contradiction with practical legal impact explanations.

---

## 📜 Disclaimer
*NyayaLens AI is designed exclusively for educational, research, and informational decision-support purposes. It does not constitute formal legal counsel or create an attorney-client relationship.*
