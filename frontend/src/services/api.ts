import {
  DocumentListItem,
  DocumentDetail,
  ClauseItem,
  RiskItem,
  ObligationItem,
  ComplianceItem,
  ComparisonResponse,
  DashboardKPIs,
  AIInsightItem
} from '../types';

const API_BASE = '/api/v1';

export async function fetchDashboardKPIs(): Promise<DashboardKPIs> {
  const res = await fetch(`${API_BASE}/analytics/dashboard-kpis`);
  if (!res.ok) throw new Error('Failed to fetch KPIs');
  return res.json();
}

export async function fetchAIInsights(): Promise<AIInsightItem[]> {
  const res = await fetch(`${API_BASE}/analytics/ai-insights`);
  if (!res.ok) throw new Error('Failed to fetch insights');
  return res.json();
}

export async function fetchDocuments(): Promise<DocumentListItem[]> {
  const res = await fetch(`${API_BASE}/documents`);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return res.json();
}

export async function fetchDocumentDetail(id: number): Promise<DocumentDetail> {
  const res = await fetch(`${API_BASE}/documents/${id}`);
  if (!res.ok) throw new Error('Failed to fetch document detail');
  return res.json();
}

export async function fetchDocumentClauses(docId: number): Promise<ClauseItem[]> {
  const res = await fetch(`${API_BASE}/documents/${docId}/clauses`);
  if (!res.ok) throw new Error('Failed to fetch document clauses');
  return res.json();
}

export async function fetchDocumentRisks(docId: number): Promise<RiskItem[]> {
  const res = await fetch(`${API_BASE}/analysis/risks/${docId}`);
  if (!res.ok) throw new Error('Failed to fetch document risks');
  return res.json();
}

export async function submitRiskFeedback(riskId: number, feedback: string) {
  const res = await fetch(`${API_BASE}/analysis/risk-feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ risk_id: riskId, feedback })
  });
  return res.json();
}

export async function fetchDocumentObligations(docId: number): Promise<ObligationItem[]> {
  const res = await fetch(`${API_BASE}/obligations/${docId}`);
  if (!res.ok) throw new Error('Failed to fetch obligations');
  return res.json();
}

export async function fetchDocumentCompliance(docId: number): Promise<ComplianceItem[]> {
  const res = await fetch(`${API_BASE}/compliance/${docId}`);
  if (!res.ok) throw new Error('Failed to fetch compliance');
  return res.json();
}

export async function compareDocuments(doc1Id: number, doc2Id: number): Promise<ComparisonResponse> {
  const res = await fetch(`${API_BASE}/comparison`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ doc1_id: doc1Id, doc2_id: doc2Id })
  });
  if (!res.ok) throw new Error('Failed to compare documents');
  return res.json();
}

export async function queryDocumentQA(docId: number, question: string, language: string = 'en') {
  const res = await fetch(`${API_BASE}/assistant/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ document_id: docId, question, language })
  });
  if (!res.ok) throw new Error(`Assistant query failed: ${res.status} ${res.statusText}`);
  return res.json();
}

export async function simplifyText(text: string, language: string = 'en') {
  const res = await fetch(`${API_BASE}/assistant/simplify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, language })
  });
  return res.json();
}

export async function uploadDocument(file: File, title?: string): Promise<DocumentDetail> {
  const formData = new FormData();
  formData.append('file', file);
  if (title) formData.append('title', title);

  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Upload failed');
  return res.json();
}

export async function deleteDocument(docId: number) {
  const res = await fetch(`${API_BASE}/documents/${docId}`, { method: 'DELETE' });
  return res.json();
}
