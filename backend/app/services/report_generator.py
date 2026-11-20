import io
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

DISCLAIMER_TEXT = (
    "LEGAL DISCLAIMER: NyayaLens AI provides automated analytical decision-support and information extraction. "
    "This document does NOT constitute formal legal advice, solicitation, or creation of an attorney-client relationship. "
    "Independent verification by a qualified legal professional is advised before executing or contesting legal instruments."
)

def generate_pdf_report(doc_data: Dict[str, Any], risks: List[Dict[str, Any]], obligations: List[Dict[str, Any]], compliance: List[Dict[str, Any]]) -> bytes:
    """
    Generate professional downloadable PDF audit report.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=12
    )
    heading2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#334155')
    )
    disclaimer_style = ParagraphStyle(
        'Disclaimer',
        parent=styles['Italic'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#64748B')
    )

    story = []

    # Title & Header
    story.append(Paragraph(f"NyayaLens AI – Legal Intelligence Audit Report", title_style))
    story.append(Paragraph(f"<b>Document Title:</b> {doc_data.get('title', 'Legal Document')}", body_style))
    story.append(Paragraph(f"<b>Classification:</b> {doc_data.get('doc_type', 'Contract')} (Confidence: {int(doc_data.get('classification_confidence', 0.95)*100)}%)", body_style))
    story.append(Paragraph(f"<b>Audited Status:</b> {doc_data.get('status', 'Reviewed')}", body_style))
    story.append(Spacer(1, 10))

    # Section 1: Risks Flagged
    story.append(Paragraph("1. Clause-Level Legal Risk Findings", heading2_style))
    if risks:
        risk_table_data = [["Risk Category", "Severity", "Clause Ref", "Analysis & Legal Exposure"]]
        for r in risks[:6]:
            risk_table_data.append([
                Paragraph(r.get("title", "Risk"), body_style),
                Paragraph(r.get("severity", "Medium"), body_style),
                Paragraph(r.get("clause_reference", "Clause"), body_style),
                Paragraph(r.get("explanation", "")[:120] + "...", body_style)
            ])
        t_risks = Table(risk_table_data, colWidths=[130, 65, 75, 270])
        t_risks.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_risks)
    else:
        story.append(Paragraph("No severe contractual risks flagged during audit.", body_style))

    story.append(Spacer(1, 12))

    # Section 2: Obligations & Deadlines
    story.append(Paragraph("2. Key Obligations & Deadlines", heading2_style))
    if obligations:
        ob_table_data = [["Responsible Party", "Action Required", "Deadline", "Amount"]]
        for o in obligations[:5]:
            ob_table_data.append([
                Paragraph(o.get("responsible_party", "Party"), body_style),
                Paragraph(o.get("action", "")[:100], body_style),
                Paragraph(o.get("deadline_text", "Specified"), body_style),
                Paragraph(o.get("amount", "N/A"), body_style)
            ])
        t_ob = Table(ob_table_data, colWidths=[100, 240, 120, 80])
        t_ob.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_ob)

    story.append(Spacer(1, 14))

    # Section 3: Statutory Compliance
    story.append(Paragraph("3. Indian Statutory Compliance Audit", heading2_style))
    if compliance:
        comp_table_data = [["Statute", "Section", "Status", "Finding"]]
        for c in compliance[:5]:
            comp_table_data.append([
                Paragraph(c.get("statute_name", "")[:30], body_style),
                Paragraph(c.get("section_reference", "")[:35], body_style),
                Paragraph(c.get("status", "Compliant"), body_style),
                Paragraph(c.get("details", "")[:120] + "...", body_style)
            ])
        t_comp = Table(comp_table_data, colWidths=[120, 130, 80, 210])
        t_comp.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('PADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(t_comp)

    story.append(Spacer(1, 16))
    story.append(Paragraph(DISCLAIMER_TEXT, disclaimer_style))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def generate_markdown_report(doc_data: Dict[str, Any], risks: List[Dict[str, Any]], obligations: List[Dict[str, Any]], compliance: List[Dict[str, Any]]) -> str:
    """
    Generate downloadable Markdown briefing report.
    """
    lines = [
        f"# NyayaLens AI – Legal Intelligence Audit Report",
        f"**Document Title:** {doc_data.get('title', 'Legal Document')}",
        f"**Document Type:** {doc_data.get('doc_type', 'Contract')} (Confidence: {int(doc_data.get('classification_confidence', 0.95)*100)}%)",
        f"**Audit Status:** {doc_data.get('status', 'Reviewed')}\n",
        f"---",
        f"## 1. Clause-Level Risk Detection"
    ]

    for r in risks:
        lines.append(f"### ⚠️ {r.get('title', 'Risk')} [{r.get('severity', 'Medium')}]")
        lines.append(f"- **Clause Reference:** {r.get('clause_reference', 'Clause')} (Page {r.get('page_number', 1)})")
        lines.append(f"- **Confidence:** {int(r.get('confidence', 0.9)*100)}%")
        lines.append(f"- **Analysis:** {r.get('explanation', '')}")
        lines.append(f"- **Recommended Remediation:** {r.get('remediation', '')}\n")

    lines.append("## 2. Key Obligations & Deadlines Schedule")
    for o in obligations:
        lines.append(f"- **{o.get('responsible_party', 'Party')}:** {o.get('action', '')}")
        lines.append(f"  - Deadline: {o.get('deadline_text', '')} | Amount: {o.get('amount', 'N/A')}")

    lines.append("\n## 3. Indian Statutory Compliance Audit")
    for c in compliance:
        lines.append(f"- **{c.get('statute_name', '')}** ({c.get('section_reference', '')}): **{c.get('status', 'Compliant')}**")
        lines.append(f"  - {c.get('details', '')}")

    lines.append("\n---\n> *" + DISCLAIMER_TEXT + "*")
    return "\n".join(lines)
