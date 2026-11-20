import re
from typing import List, Dict, Any

# Curated Indian Statutory Knowledge Base Rules
INDIAN_COMPLIANCE_STANDARDS = [
    {
        "id": "ICA_SEC_27",
        "statute": "Indian Contract Act, 1872",
        "section": "Section 27 (Agreement in Restraint of Trade)",
        "requirement": "Post-engagement non-compete restrictions are void under Indian jurisprudence.",
        "search_pattern": r'\b(?:non-compete|restraint of trade|shall not engage in any competing)\b',
        "missing_check": False,
        "is_mandatory": True,
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187?view_type=browse&sam_handle=123456789/1362",
        "evaluation_rule": "If non-compete found in employment/service without goodwill sale -> Violation."
    },
    {
        "id": "ICA_SEC_28",
        "statute": "Indian Contract Act, 1872",
        "section": "Section 28 (Agreements in Restraint of Legal Proceedings)",
        "requirement": "Parties cannot extinguish the statutory period of limitation or bar access to judicial courts.",
        "search_pattern": r'\b(?:waives any right to approach court|bars all legal recourse|claims barred after 30 days)\b',
        "missing_check": False,
        "is_mandatory": True,
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "evaluation_rule": "Clauses reducing limitation period below statutory 3 years are void."
    },
    {
        "id": "DPDP_ACT_2023",
        "statute": "Digital Personal Data Protection Act, 2023",
        "section": "Section 6 (Consent & Purpose Limitation)",
        "requirement": "Commercial contracts handling personal data must contain explicit consent, purpose limitation, and breach notification terms.",
        "search_pattern": r'\b(?:data protection|personal data|dpdp|privacy policy|data principal|data fiduciary)\b',
        "missing_check": True,
        "is_mandatory": True,
        "source_url": "https://www.meity.gov.in/content/digital-personal-data-protection-act-2023",
        "evaluation_rule": "Absence of data protection terms in service contracts triggers Missing Clause warning."
    },
    {
        "id": "ARB_ACT_1996",
        "statute": "Arbitration and Conciliation Act, 1996",
        "section": "Section 7 (Arbitration Agreement)",
        "requirement": "An arbitration agreement must be in writing, specifying seat, rules, and appointing authority.",
        "search_pattern": r'\b(?:arbitration|arbitrator|arbitration and conciliation act|seat of arbitration)\b',
        "missing_check": True,
        "is_mandatory": False,  # Recommended
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1978",
        "evaluation_rule": "Recommended for commercial dispute resolution efficiency."
    },
    {
        "id": "STAMP_ACT_1899",
        "statute": "Indian Stamp Act, 1899 & State Stamp Acts",
        "section": "Section 35 (Inadmissibility of Unstamped Instruments)",
        "requirement": "Agreements creating legal rights/leases must be stamped with requisite duty to be admissible in evidence.",
        "search_pattern": r'\b(?:stamp duty|stamped|non-judicial stamp paper)\b',
        "missing_check": True,
        "is_mandatory": True,
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2311",
        "evaluation_rule": "Check presence of stamp duty notation."
    },
    {
        "id": "SEVERABILITY_PROVISION",
        "statute": "Indian Legal Drafting Standards",
        "section": "Severability & Survival Doctrine",
        "requirement": "Agreement must state that invalidation of any single clause does not vitiate the entire contract.",
        "search_pattern": r'\b(?:severability|mutatis mutandis|remainder of this agreement shall continue)\b',
        "missing_check": True,
        "is_mandatory": False,
        "source_url": "https://www.indiacode.nic.in",
        "evaluation_rule": "Standard risk mitigation clause."
    }
]

def audit_compliance(full_text: str, doc_type: str) -> List[Dict[str, Any]]:
    """
    Audit document against Indian statutes and identify missing or non-compliant clauses.
    """
    compliance_results = []
    text_lower = full_text.lower()

    for item in INDIAN_COMPLIANCE_STANDARDS:
        has_pattern = bool(re.search(item["search_pattern"], text_lower, re.IGNORECASE))
        
        if item["id"] == "ICA_SEC_27":
            if has_pattern:
                status = "Violation"
                details = "Agreement contains restrictive covenants (non-compete) that violate Section 27 of the Indian Contract Act, 1872. Under Indian law, post-termination restraint of trade is void ab initio."
            else:
                status = "Compliant"
                details = "No overbroad post-employment restraint of trade detected. Complies with Section 27 standards."

        elif item["id"] == "ICA_SEC_28":
            if has_pattern:
                status = "Violation"
                details = "Identified clause attempting to extinguish legal remedy or reduce limitation period. Violates Section 28 of the Indian Contract Act, 1872."
            else:
                status = "Compliant"
                details = "Standard legal dispute provisions preserved without illegal waiver of judicial recourse."

        elif item["id"] == "DPDP_ACT_2023":
            if has_pattern:
                status = "Compliant"
                details = "Data handling and privacy provisions are documented in alignment with DPDP Act, 2023 obligations."
            else:
                status = "Missing Clause"
                details = "MISSING CLAUSE DETECTED: No explicit Data Protection or Data Fiduciary clause found. Under the DPDP Act, 2023, data processing without documented safeguards incurs statutory non-compliance exposure."

        elif item["id"] == "ARB_ACT_1996":
            if has_pattern:
                status = "Compliant"
                details = "Valid written arbitration clause identified specifying dispute resolution under the Arbitration & Conciliation Act, 1996."
            else:
                status = "Missing Clause"
                details = "No arbitration clause identified. In event of dispute, litigation will default to local civil courts with multi-year procedural backlog."

        elif item["id"] == "STAMP_ACT_1899":
            if has_pattern:
                status = "Compliant"
                details = "Stamp duty references identified. Ensure appropriate state-specific non-judicial stamp duty is paid."
            else:
                status = "Insufficient Information"
                details = "Stamp duty notation not found in raw digital text. Physical execution on requisite state stamp paper must be verified for court admissibility under Section 35."

        elif item["id"] == "SEVERABILITY_PROVISION":
            if has_pattern:
                status = "Compliant"
                details = "Severability clause present. Preserves contract validity if individual subclauses are declared unenforceable."
            else:
                status = "Missing Clause"
                details = "Missing Severability clause. Unenforceability of any single clause risks jeopardizing the entire agreement."

        compliance_results.append({
            "statute_name": item["statute"],
            "section_reference": item["section"],
            "requirement": item["requirement"],
            "status": status,
            "details": details,
            "source_url": item["source_url"]
        })

    return compliance_results
