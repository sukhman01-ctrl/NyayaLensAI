export interface DocumentListItem {
  id: number;
  title: string;
  filename: string;
  file_type: string;
  page_count: number;
  status: 'Reviewed' | 'Processing' | 'Risk Found';
  doc_type: string;
  classification_confidence: number;
  uploaded_at: string;
  clauses_flagged: number;
}

export interface DocumentDetail {
  id: number;
  title: string;
  filename: string;
  file_type: string;
  file_size_bytes: number;
  page_count: number;
  status: string;
  doc_type: string;
  classification_confidence: number;
  uploaded_at: string;
  parties_json: string;
  effective_date: string;
  governing_law: string;
  jurisdiction: string;
  raw_text: string;
}

export interface ClauseItem {
  id: number;
  document_id: number;
  clause_number: string;
  heading: string;
  text: string;
  page_number: number;
  order_index: number;
}

export interface RiskItem {
  id: number;
  document_id: number;
  title: string;
  category: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  confidence: number;
  explanation: string;
  remediation: string;
  clause_reference: string;
  page_number: number;
  user_feedback?: string | null;
}

export interface ObligationItem {
  id: number;
  document_id: number;
  responsible_party: string;
  action: string;
  deadline_text: string;
  due_date?: string | null;
  amount: string;
  category: string;
  is_ambiguous: boolean;
  clause_reference: string;
  page_number: number;
}

export interface ComplianceItem {
  id: number;
  document_id: number;
  statute_name: string;
  section_reference: string;
  requirement: string;
  status: 'Compliant' | 'Violation' | 'Missing Clause' | 'Insufficient Information';
  details: string;
  source_url: string;
}

export interface ComparisonResponse {
  doc1_title: string;
  doc2_title: string;
  total_modifications: number;
  contradictions_count: number;
  diff_items: {
    change_type: 'MODIFIED' | 'ADDED' | 'REMOVED' | 'IDENTICAL';
    clause_title: string;
    doc1_text?: string;
    doc2_text?: string;
    doc1_clause_ref?: string;
    doc2_clause_ref?: string;
    impact_explanation: string;
    is_contradiction: boolean;
  }[];
  summary: string;
}

export interface DashboardKPIs {
  docs_analyzed: { value: string; trend: string };
  risks_flagged: { value: string; trend: string };
  review_time_saved: { value: string; trend: string };
  ai_accuracy: { value: string; trend: string };
}

export interface AIInsightItem {
  id: number;
  title: string;
  type: string;
  description: string;
  confidence: number;
  badge_color: string;
}
