import os
import re
from typing import List, Dict, Any, Tuple
from pathlib import Path

def extract_text_with_pages(file_path: Path) -> List[Dict[str, Any]]:
    """
    Extract text while preserving page numbers and paragraph chunks.
    Returns: List[{"page": int, "text": str}]
    """
    ext = file_path.suffix.lower()
    pages_data = []

    if ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            for page_idx, page in enumerate(doc):
                text = page.get_text("text")
                if text.strip():
                    pages_data.append({"page": page_idx + 1, "text": text.strip()})
            if pages_data:
                return pages_data
        except Exception:
            pass

        # Fallback to PyPDF
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(file_path))
            for page_idx, page in enumerate(reader.pages):
                text = page.extract_text() or ""
                if text.strip():
                    pages_data.append({"page": page_idx + 1, "text": text.strip()})
            if pages_data:
                return pages_data
        except Exception as e:
            print(f"[Extractor] PDF extraction error: {e}")

    elif ext in [".docx", ".doc"]:
        try:
            import docx
            doc = docx.Document(str(file_path))
            text_chunks = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
            full_text = "\n\n".join(text_chunks)
            # Estimate pages (~350 words per page)
            words = full_text.split()
            page_size = 350
            for i in range(0, max(len(words), 1), page_size):
                page_words = words[i:i+page_size]
                pages_data.append({
                    "page": (i // page_size) + 1,
                    "text": " ".join(page_words)
                })
            return pages_data
        except Exception as e:
            print(f"[Extractor] DOCX extraction error: {e}")

    # Plain text / fallback
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
            # Split into estimated pages
            paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
            current_page = 1
            current_chunk = []
            word_acc = 0
            
            for p in paragraphs:
                words_in_p = len(p.split())
                current_chunk.append(p)
                word_acc += words_in_p
                if word_acc > 320:
                    pages_data.append({"page": current_page, "text": "\n\n".join(current_chunk)})
                    current_page += 1
                    current_chunk = []
                    word_acc = 0
            
            if current_chunk:
                pages_data.append({"page": current_page, "text": "\n\n".join(current_chunk)})

            if not pages_data:
                pages_data.append({"page": 1, "text": content})
            return pages_data
    except Exception as e:
        print(f"[Extractor] File read error: {e}")
        return [{"page": 1, "text": "Error extracting text from document."}]


def segment_clauses(pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Segment pages into distinct numbered legal clauses.
    Returns: List[{"clause_number": str, "heading": str, "text": str, "page_number": int, "order_index": int}]
    """
    clauses = []
    order_index = 0

    # Patterns for legal clause numbering:
    # "1. ", "Clause 1. ", "1.1 ", "Section 2. ", "Article 3: ", "(a) ", "VIII. "
    clause_pattern = re.compile(
        r'(?:\n|^)(?:Clause\s+|Section\s+|Article\s+)?(\d+(?:\.\d+)*|[A-Z]\.|\([a-z0-9]+\))\s*[:.\-]?\s+([A-Z][A-Za-z0-9\s,\'-]{2,50})?(?:\n|:|\.\s+)',
        re.MULTILINE
    )

    for page_item in pages_data:
        page_num = page_item["page"]
        text = page_item["text"]

        splits = re.split(r'\n\n(?=(?:Clause\s+|Section\s+|Article\s+|\d+\.\s+|\([a-z]\)\s+))', text)
        
        if len(splits) > 1:
            for s in splits:
                s_clean = s.strip()
                if not s_clean:
                    continue
                lines = s_clean.split("\n")
                first_line = lines[0].strip()
                match = re.match(r'^(?:Clause\s+|Section\s+|Article\s+)?(\d+(?:\.\d+)*|[A-Z]\.|\([a-z0-9]+\))?\s*[:.\-]?\s*(.*)$', first_line, re.IGNORECASE)
                
                num_part = "Clause"
                heading_part = "General Clause"
                if match:
                    if match.group(1):
                        num_part = f"Clause {match.group(1)}"
                    if match.group(2) and len(match.group(2)) < 50:
                        heading_part = match.group(2).strip()

                clauses.append({
                    "clause_number": num_part,
                    "heading": heading_part,
                    "text": s_clean,
                    "page_number": page_num,
                    "order_index": order_index
                })
                order_index += 1
        else:
            # Paragraph level fallback
            paras = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 30]
            for p in paras:
                clauses.append({
                    "clause_number": f"Clause {order_index + 1}",
                    "heading": p[:45] + "...",
                    "text": p,
                    "page_number": page_num,
                    "order_index": order_index
                })
                order_index += 1

    return clauses
