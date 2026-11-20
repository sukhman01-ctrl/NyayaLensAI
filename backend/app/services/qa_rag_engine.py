import re
from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------------------------
# Intent → plain-English answer templates
# ---------------------------------------------------------------------------
_SIGN_PATTERNS = re.compile(
    r'\b(sign|should i|safe to sign|recommend|agree|accept)\b', re.IGNORECASE)
_RISK_PATTERNS = re.compile(
    r'\b(risk|danger|problem|issue|concern|liable|liability|harmful|bad|unfair|one.sided)\b',
    re.IGNORECASE)
_PAYMENT_PATTERNS = re.compile(
    r'\b(pay|payment|fee|salary|compensation|amount|cost|price|money|rupee|inr)\b',
    re.IGNORECASE)
_TERMINATE_PATTERNS = re.compile(
    r'\b(terminat|end|exit|quit|leave|cancel|break|stop)\b', re.IGNORECASE)
_DEADLINE_PATTERNS = re.compile(
    r'\b(deadline|due|when|time|days|notice|period|duration|expir)\b', re.IGNORECASE)
_PARTY_PATTERNS = re.compile(
    r'\b(who|parties|company|contractor|employer|employee|provider|client|vendor)\b',
    re.IGNORECASE)


def _simplify_clause_text(text: str, max_sentences: int = 3) -> str:
    """Return at most max_sentences from clause text, stripped of legalese filler."""
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    # Remove very short or boilerplate sentences
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
    return ' '.join(sentences[:max_sentences])


def _build_plain_answer(question: str, clause: Dict[str, Any],
                         all_clauses: List[Dict[str, Any]]) -> str:
    """
    Produce a short, plain-English answer based on question intent + clause content.
    """
    q = question.lower()
    text = clause.get("text", "")
    heading = clause.get("heading", "")
    clause_ref = clause.get("clause_number", "the relevant clause")
    page_num = clause.get("page_number", 1)
    snippet = _simplify_clause_text(text, max_sentences=2)

    # --- Should I sign? ---
    if _SIGN_PATTERNS.search(q):
        # Count risk indicators across all clauses
        risk_words = ["shall not", "liable", "indemnify", "penalty", "forfeit",
                      "terminate", "non-compete", "restraint", "unilateral"]
        risk_count = sum(
            1 for c in all_clauses
            for w in risk_words if w in c.get("text", "").lower()
        )
        if risk_count >= 3:
            return (
                f"⚠️ **Be careful before signing.** This document contains {risk_count} "
                f"potentially risky clauses (e.g., liability, termination, or restraint terms). "
                f"Review the flagged risks in the 'Clause Risks' tab and consider getting legal advice. "
                f"Key concern from {clause_ref} (Page {page_num}): {snippet}"
            )
        else:
            return (
                f"✅ **The document looks relatively straightforward.** "
                f"No major red flags were detected automatically. "
                f"Still, read all clauses carefully before signing. "
                f"From {clause_ref} (Page {page_num}): {snippet}"
            )

    # --- Risk / danger questions ---
    if _RISK_PATTERNS.search(q):
        return (
            f"⚠️ **Potential risk found** in {clause_ref} (Page {page_num}):\n\n"
            f"{snippet}\n\n"
            f"In plain English: this clause may impose obligations or liabilities on you. "
            f"Check the 'Clause Risks' tab for a detailed breakdown of all flagged risks."
        )

    # --- Payment questions ---
    if _PAYMENT_PATTERNS.search(q):
        return (
            f"💰 **Payment terms** are addressed in {clause_ref} (Page {page_num}):\n\n"
            f"{snippet}\n\n"
            f"In plain English: this covers how and when money is to be paid. "
            f"Look for specific amounts, due dates, and penalty clauses."
        )

    # --- Termination questions ---
    if _TERMINATE_PATTERNS.search(q):
        return (
            f"🔚 **Termination terms** are in {clause_ref} (Page {page_num}):\n\n"
            f"{snippet}\n\n"
            f"In plain English: this explains how and when either party can end the agreement. "
            f"Check notice period requirements and any penalties for early exit."
        )

    # --- Deadline / duration questions ---
    if _DEADLINE_PATTERNS.search(q):
        return (
            f"📅 **Timeline / deadline** found in {clause_ref} (Page {page_num}):\n\n"
            f"{snippet}\n\n"
            f"In plain English: this sets a time limit or notice period. "
            f"Missing this deadline may have legal consequences."
        )

    # --- Who are the parties? ---
    if _PARTY_PATTERNS.search(q):
        parties = [c.get("text", "") for c in all_clauses[:1]]
        party_snippet = _simplify_clause_text(parties[0] if parties else text, 2)
        return (
            f"👥 **Parties to the agreement** ({clause_ref}, Page {page_num}):\n\n"
            f"{party_snippet}\n\n"
            f"In plain English: these are the people or companies who are legally bound by this document."
        )

    # --- Generic / fallback ---
    return (
        f"📄 **{clause_ref}{' — ' + heading if heading else ''}** (Page {page_num}):\n\n"
        f"{snippet}\n\n"
        f"In plain English: {_reword_as_plain(snippet)}"
    )


def _reword_as_plain(text: str) -> str:
    """Very lightweight legalese → plain English substitution."""
    replacements = [
        (r'\bhereinafter\b', 'from now on called'),
        (r'\bwhereas\b', 'since'),
        (r'\bshall\b', 'must'),
        (r'\bnotwithstanding\b', 'despite'),
        (r'\bforthwith\b', 'immediately'),
        (r'\bthereof\b', 'of it'),
        (r'\btherein\b', 'in it'),
        (r'\bhereof\b', 'of this document'),
        (r'\binter alia\b', 'among other things'),
        (r'\bmutatis mutandis\b', 'with necessary changes'),
    ]
    result = text
    for pattern, replacement in replacements:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


class DocumentRAGEngine:
    """
    In-memory RAG retriever that returns short, plain-English answers
    grounded in document clauses.
    """
    def __init__(self, clauses: List[Dict[str, Any]]):
        self.clauses = clauses
        self.texts = [c["text"] for c in clauses]
        if self.texts:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
            self.matrix = self.vectorizer.fit_transform(self.texts)
        else:
            self.vectorizer = None
            self.matrix = None

    def _find_clause_by_number(self, question: str) -> Optional[int]:
        """Direct lookup when user asks about a specific clause/section number."""
        pattern = re.search(
            r'(?:clause|section|cl\.?|sec\.?|§)\s*(\d+(?:\.\d+)?)',
            question,
            re.IGNORECASE
        )
        if pattern:
            target = pattern.group(1).lower()
            for i, c in enumerate(self.clauses):
                cn = str(c.get("clause_number", "")).lower()
                if (cn == target or cn == f"clause {target}"
                        or cn == f"section {target}"
                        or re.search(r'\b' + re.escape(target) + r'\b', cn)):
                    return i
        return None

    def query(self, question: str, top_k: int = 3) -> Dict[str, Any]:
        if self.matrix is None or not self.texts:
            return {
                "answer": "No clauses found in this document. Please upload a valid legal document first.",
                "confidence": 0.0,
                "clause_citations": [],
                "page_references": [],
                "evidence_text": ""
            }

        # 1. Direct clause-number lookup
        direct_idx = self._find_clause_by_number(question)
        if direct_idx is not None:
            best_clause = self.clauses[direct_idx]
            answer = _build_plain_answer(question, best_clause, self.clauses)
            return {
                "answer": answer,
                "confidence": 0.96,
                "clause_citations": [best_clause.get("clause_number", "Clause")],
                "page_references": [best_clause.get("page_number", 1)],
                "evidence_text": _simplify_clause_text(best_clause["text"], 2)
            }

        # 2. TF-IDF semantic retrieval
        q_vec = self.vectorizer.transform([question])
        scores = cosine_similarity(q_vec, self.matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)

        top_matches = [idx for idx, s in ranked[:top_k] if s > 0.005]
        if not top_matches:
            top_matches = [ranked[0][0]]  # Always return best match

        best_idx = top_matches[0]
        best_score = float(ranked[0][1])
        best_clause = self.clauses[best_idx]

        answer = _build_plain_answer(question, best_clause, self.clauses)

        return {
            "answer": answer,
            "confidence": min(0.96, max(0.72, 0.70 + best_score * 0.5)),
            "clause_citations": [best_clause.get("clause_number", "Clause")],
            "page_references": [best_clause.get("page_number", 1)],
            "evidence_text": _simplify_clause_text(best_clause["text"], 2)
        }
