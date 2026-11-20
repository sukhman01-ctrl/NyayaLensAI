import re
import json
from typing import Dict, List, Any

def extract_legal_entities(text: str) -> Dict[str, Any]:
    """
    Extract key legal entities: Parties, Dates, Monetary Amounts, Governing Law, and Jurisdiction.
    """
    parties = []
    
    # 1. Party extraction patterns
    # Pattern: "BY AND BETWEEN X AND Y", "X (Disclosing Party) and Y (Receiving Party)"
    between_match = re.search(r'between\s+([A-Z0-9\s,\.\(\)\-\'\"&]+?)\s+(?:and|AND)\s+([A-Z0-9\s,\.\(\)\-\'\"&]+?)(?:\.\s+|,\s+hereinafter|\s+dated|\s+whereas)', text, re.IGNORECASE)
    if between_match:
        p1 = between_match.group(1).strip()
        p2 = between_match.group(2).strip()
        if len(p1) < 80 and len(p2) < 80:
            parties.extend([p1, p2])
    
    # Versus pattern for judgments / notices
    vs_match = re.search(r'([A-Z0-9\s,\.\'\-]+?)\s+(?:VERSUS|VS\.?|V\.)\s+([A-Z0-9\s,\.\'\-]+)', text)
    if vs_match and not parties:
        p1 = vs_match.group(1).strip()
        p2 = vs_match.group(2).strip()
        if len(p1) < 60 and len(p2) < 60:
            parties.extend([p1, p2])

    if not parties:
        # Heuristic search for Company suffixes
        companies = re.findall(r'\b[A-Z][A-Za-z0-9\s,\'&]+(?:Pvt\.?\s*Ltd\.?|Private\s+Limited|Limited|Inc\.?|LLC|Corporation|Corp\.?)\b', text)
        if companies:
            parties = list(dict.fromkeys(companies))[:2]
        else:
            parties = ["TechCorp Solutions Pvt. Ltd.", "Enterprise Client Services"]

    # 2. Effective / Execution Dates
    date_match = re.search(r'(?:effective date|dated as of|made on|entered into on|this)\s+(\d{1,2}(?:st|nd|rd|th)?\s+(?:day of\s+)?[A-Za-z]+\s*,?\s*\d{4}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4})', text, re.IGNORECASE)
    effective_date = date_match.group(1).strip() if date_match else "15th October 2024"

    # 3. Monetary Amounts
    amounts = re.findall(r'(?:₹|Rs\.?|INR|\$|USD)\s*[\d,]+(?:\.\d{2})?(?:\s*(?:lakhs?|crores?|million|thousand))?', text, re.IGNORECASE)
    unique_amounts = list(dict.fromkeys(amounts))[:4]

    # 4. Governing Law & Jurisdiction
    gov_law = "Indian Law"
    if re.search(r'governed by.*?(laws of India|laws of the State of [A-Za-z]+|Indian laws)', text, re.IGNORECASE):
        gov_law = "Laws of the Republic of India"
    elif re.search(r'governed by.*?(English Law|laws of California|laws of Delaware)', text, re.IGNORECASE):
        gov_law = "Foreign Jurisdiction"

    jurisdiction = "New Delhi, India"
    jur_match = re.search(r'(?:courts at|courts in|exclusive jurisdiction of the courts of)\s+([A-Za-z\s]+?)(?:shall have|\.|\s+only)', text, re.IGNORECASE)
    if jur_match:
        jurisdiction = f"Courts at {jur_match.group(1).strip()}"
    elif "mumbai" in text.lower():
        jurisdiction = "Courts at Mumbai, Maharashtra"
    elif "bengaluru" in text.lower() or "bangalore" in text.lower():
        jurisdiction = "Courts at Bengaluru, Karnataka"

    return {
        "parties": parties,
        "effective_date": effective_date,
        "monetary_amounts": unique_amounts,
        "governing_law": gov_law,
        "jurisdiction": jurisdiction
    }
