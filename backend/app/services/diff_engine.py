import re
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compare_documents(doc1_clauses: List[Dict[str, Any]], doc2_clauses: List[Dict[str, Any]], doc1_title: str, doc2_title: str) -> Dict[str, Any]:
    """
    Semantically align clauses between Doc 1 and Doc 2 and detect contradictions.
    """
    diff_items = []
    contradictions_count = 0

    doc1_texts = [c["text"] for c in doc1_clauses]
    doc2_texts = [c["text"] for c in doc2_clauses]

    if not doc1_texts or not doc2_texts:
        return {
            "doc1_title": doc1_title,
            "doc2_title": doc2_title,
            "total_modifications": 0,
            "contradictions_count": 0,
            "diff_items": [],
            "summary": "Insufficient clauses found to execute cross-document semantic comparison."
        }

    # Vectorize all clauses together
    all_texts = doc1_texts + doc2_texts
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    m1 = tfidf_matrix[:len(doc1_texts)]
    m2 = tfidf_matrix[len(doc1_texts):]

    sim_matrix = cosine_similarity(m1, m2)

    matched_doc2_indices = set()

    for i, c1 in enumerate(doc1_clauses):
        best_j = -1
        best_sim = 0.0

        for j, c2 in enumerate(doc2_clauses):
            score = sim_matrix[i, j]
            if score > best_sim:
                best_sim = score
                best_j = j

        c1_ref = c1.get("clause_number", f"Clause {i+1}")
        c1_text = c1["text"]

        if best_sim >= 0.85:
            # Substantially identical
            continue
        elif best_sim >= 0.35 and best_j != -1:
            matched_doc2_indices.add(best_j)
            c2 = doc2_clauses[best_j]
            c2_ref = c2.get("clause_number", f"Clause {best_j+1}")
            c2_text = c2["text"]

            # Contradiction analysis
            is_contradiction = False
            impact = "Wording adjusted for clarity."

            # Check amounts contradiction
            amt1 = set(re.findall(r'(?:₹|Rs\.?|INR|\$|USD)\s*[\d,]+', c1_text))
            amt2 = set(re.findall(r'(?:₹|Rs\.?|INR|\$|USD)\s*[\d,]+', c2_text))
            if amt1 and amt2 and amt1 != amt2:
                is_contradiction = True
                impact = f"Financial Contradiction: Compensation modified from {list(amt1)[0]} to {list(amt2)[0]}."
                contradictions_count += 1

            # Check notice periods contradiction
            n1 = re.findall(r'(\d+)\s*days?', c1_text, re.IGNORECASE)
            n2 = re.findall(r'(\d+)\s*days?', c2_text, re.IGNORECASE)
            if n1 and n2 and n1[0] != n2[0]:
                is_contradiction = True
                impact = f"Notice Period Discrepancy: Altered from {n1[0]} days to {n2[0]} days, creating asymmetric operational risk."
                contradictions_count += 1

            if not is_contradiction:
                impact = "Material modification: Substantive terms, risk allocation, or scope altered between revisions."

            diff_items.append({
                "change_type": "MODIFIED",
                "clause_title": c1.get("heading", f"{c1_ref} vs {c2_ref}"),
                "doc1_text": c1_text,
                "doc2_text": c2_text,
                "doc1_clause_ref": c1_ref,
                "doc2_clause_ref": c2_ref,
                "impact_explanation": impact,
                "is_contradiction": is_contradiction
            })
        else:
            # Removed in Doc 2
            diff_items.append({
                "change_type": "REMOVED",
                "clause_title": c1.get("heading", c1_ref),
                "doc1_text": c1_text,
                "doc2_text": None,
                "doc1_clause_ref": c1_ref,
                "doc2_clause_ref": None,
                "impact_explanation": "Clause present in original document was deleted in the secondary draft. May waive key protections.",
                "is_contradiction": False
            })

    # Added in Doc 2
    for j, c2 in enumerate(doc2_clauses):
        if j not in matched_doc2_indices:
            c2_ref = c2.get("clause_number", f"Clause {j+1}")
            diff_items.append({
                "change_type": "ADDED",
                "clause_title": c2.get("heading", c2_ref),
                "doc1_text": None,
                "doc2_text": c2["text"],
                "doc1_clause_ref": None,
                "doc2_clause_ref": c2_ref,
                "impact_explanation": "New clause introduced in second document. Requires legal scrutiny before acceptance.",
                "is_contradiction": False
            })

    summary_msg = (
        f"Compared '{doc1_title}' against '{doc2_title}'. "
        f"Detected {len(diff_items)} notable clause modifications with "
        f"{contradictions_count} high-severity contradictions flagged."
    )

    return {
        "doc1_title": doc1_title,
        "doc2_title": doc2_title,
        "total_modifications": len(diff_items),
        "contradictions_count": contradictions_count,
        "diff_items": diff_items,
        "summary": summary_msg
    }
