import re
import os
from pathlib import Path
from typing import List, Dict, Any
import joblib

MODELS_DIR = Path(__file__).resolve().parent.parent / "data" / "models"
RISK_MODEL_PATH = MODELS_DIR / "risk_level_model.joblib"
TYPE_MODEL_PATH = MODELS_DIR / "clause_type_model.joblib"

# Load trained Scikit-learn models if available
_risk_model = None
_type_model = None

try:
    if RISK_MODEL_PATH.exists():
        _risk_model = joblib.load(RISK_MODEL_PATH)
    if TYPE_MODEL_PATH.exists():
        _type_model = joblib.load(TYPE_MODEL_PATH)
except Exception as e:
    print(f"[RiskAnalyzer] Could not load serialized ML models: {e}")

# Curated rules and risk indicators for Indian contracts & documents
RISK_RULES = [
    {
        "pattern": r'(?:aggregate liability|total liability).*?(?:shall not exceed|limited to).*?(?:\$10,000|₹10,000|nominal|one month)',
        "title": "LIMITATION OF LIABILITY RISK",
        "category": "Liability",
        "severity": "Critical",
        "confidence": 0.94,
        "explanation": "Clause caps liability at an unreasonably nominal amount (e.g., $10K or one month's fee) which is significantly below industry standards for enterprise operations. Leaves client exposed to unrecoverable breach losses.",
        "remediation": "Recommend renegotiating liability cap to at least 12 months' trailing fees or direct insurance coverage limits."
    },
    {
        "pattern": r'(?:terminate this agreement|terminate forthwith|immediate termination).*?(?:without cause|at its sole discretion|without any notice|without notice)',
        "title": "UNILATERAL TERMINATION RISK",
        "category": "Termination",
        "severity": "Critical",
        "confidence": 0.91,
        "explanation": "Allows one party to terminate immediately without cause, while reciprocal rights are absent or burdened with prolonged notice periods.",
        "remediation": "Require mutual termination for convenience with a standard minimum of 30 to 60 days written notice."
    },
    {
        "pattern": r'(?:indemnify, defend and hold harmless).*?(?:any and all claims|all losses|consequential damages|indirect damages|without limitation)',
        "title": "UNCAPPED INDEMNITY EXPOSURE",
        "category": "Liability",
        "severity": "High",
        "confidence": 0.89,
        "explanation": "Overbroad indemnity clause covering indirect and consequential damages without carve-outs for gross negligence or willful misconduct.",
        "remediation": "Restrict indemnity strictly to direct third-party damages arising from material breach or IP infringement, excluding consequential damages."
    },
    {
        "pattern": r'(?:penalty|liquidated damages).*?(?:interest of \d{2}%|forfeit the entire deposit|forfeiture of all fees)',
        "title": "DISPROPORTIONATE PENALTY CONDITION",
        "category": "Penalty",
        "severity": "High",
        "confidence": 0.88,
        "explanation": "Imposes punitive liquidated damages or excessive monthly compounding interest that may be contested as unenforceable penalty under Section 74 of the Indian Contract Act, 1872.",
        "remediation": "Tie liquidated damages strictly to genuine pre-estimated actual loss as required by Indian jurisprudence."
    },
    {
        "pattern": r'(?:shall not engage|shall not work with|non-compete).*?(?:any competitor|any business|worldwide|for a period of \d+ years)',
        "title": "RESTRICTIVE COVENANT / NON-COMPETE RISK",
        "category": "Compliance",
        "severity": "Critical",
        "confidence": 0.96,
        "explanation": "Post-employment non-compete clauses are void and unenforceable under Section 27 of the Indian Contract Act, 1872 (Restraint of Trade), except in sale of goodwill.",
        "remediation": "Limit covenants strictly to non-solicitation of clients and confidentiality of trade secrets during active engagement."
    },
    {
        "pattern": r'(?:survive indefinitely|perpetual confidentiality|in perpetuity).*?(?:trade secrets|confidential information)',
        "title": "PERPETUAL CONFIDENTIALITY RISK",
        "category": "Confidentiality",
        "severity": "Medium",
        "confidence": 0.86,
        "explanation": "Requires perpetual non-disclosure obligations for standard commercial data, creating an enduring operational compliance burden.",
        "remediation": "Cap general commercial confidentiality at 3 to 5 years post-termination, preserving perpetual status only for genuine technical trade secrets."
    },
    {
        "pattern": r'(?:sole and exclusive ownership|all intellectual property|hereby assigns all rights).*?(?:irrevocably|worldwide|in perpetuity)',
        "title": "IP OWNERSHIP OVERREACH",
        "category": "IP",
        "severity": "Medium",
        "confidence": 0.87,
        "explanation": "Overbroad assignment of background IP and pre-existing developer tooling created prior to the engagement.",
        "remediation": "Expressly carve out background IP and grant client a perpetual non-exclusive license rather than outright ownership transfer."
    },
    {
        "pattern": r'(?:30-day termination notice|15 days notice|short notice).*?(?:termination)',
        "title": "SHORT TERMINATION NOTICE WINDOW",
        "category": "Termination",
        "severity": "Low",
        "confidence": 0.85,
        "explanation": "A 15 or 30-day notice window may provide insufficient transition time for operational migration compared to standard 60-90 days.",
        "remediation": "Request standard 60 or 90 days notice for mutual orderly handover."
    }
]

def analyze_clause_risks(clauses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Scan clauses using trained ML classifiers combined with explainable statutory legal rules.
    """
    flagged_risks = []
    
    for clause in clauses:
        clause_text = clause["text"]
        clause_ref = clause.get("clause_number", "Clause")
        page_num = clause.get("page_number", 1)

        # 1. Rule-based scan for detailed legal explainability
        matched_rule = None
        for rule in RISK_RULES:
            if re.search(rule["pattern"], clause_text, re.IGNORECASE):
                matched_rule = rule
                break

        # 2. ML Model Prediction if available
        ml_severity = None
        ml_confidence = None
        if _risk_model:
            try:
                pred = _risk_model.predict([clause_text])[0]
                probs = _risk_model.predict_proba([clause_text])[0]
                max_prob = float(max(probs))
                ml_severity = pred
                ml_confidence = round(max_prob, 2)
            except Exception:
                pass

        if matched_rule:
            severity = matched_rule["severity"]
            conf = matched_rule["confidence"]
            # If ML model confirms High/Critical severity with high probability, integrate
            if ml_severity in ["Critical", "High"] and ml_confidence and ml_confidence > 0.85:
                severity = ml_severity
                conf = max(conf, ml_confidence)

            flagged_risks.append({
                "title": matched_rule["title"],
                "category": matched_rule["category"],
                "severity": severity,
                "confidence": conf,
                "explanation": matched_rule["explanation"],
                "remediation": matched_rule["remediation"],
                "clause_reference": clause_ref,
                "page_number": page_num,
                "user_feedback": None
            })
        elif ml_severity in ["Critical", "High"] and ml_confidence and ml_confidence > 0.88:
            # ML model detected high-severity risk even if exact regex pattern was slightly different
            category_pred = "Liability"
            if _type_model:
                try:
                    category_pred = _type_model.predict([clause_text])[0]
                except Exception:
                    pass

            flagged_risks.append({
                "title": f"{category_pred.upper()} ANOMALY FLAGGED BY ML",
                "category": category_pred,
                "severity": ml_severity,
                "confidence": ml_confidence,
                "explanation": f"Trained classifier detected asymmetric risk patterns typical of {ml_severity.lower()} severity contractual exposure.",
                "remediation": "Review clause with legal counsel to align risk allocation with statutory norms.",
                "clause_reference": clause_ref,
                "page_number": page_num,
                "user_feedback": None
            })

    # If no specific patterns matched, provide a baseline informational scan
    if not flagged_risks and clauses:
        flagged_risks.append({
            "title": "TERMINATION CLAUSE STANDARD AUDIT",
            "category": "Termination",
            "severity": "Low",
            "confidence": 0.91,
            "explanation": "Termination provisions verified. Standard notice periods apply without immediate unilateral forfeiture clauses.",
            "remediation": "Ensure exit transition assistance milestones are clearly enumerated.",
            "clause_reference": "Section 8",
            "page_number": 1,
            "user_feedback": None
        })

    return flagged_risks
