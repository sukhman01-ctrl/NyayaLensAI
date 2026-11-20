import React, { useState, useEffect } from 'react';
import { 
  DocumentDetail, 
  ClauseItem, 
  RiskItem, 
  ObligationItem, 
  ComplianceItem 
} from '../types';
import { 
  fetchDocumentClauses, 
  fetchDocumentRisks, 
  fetchDocumentObligations, 
  fetchDocumentCompliance,
  submitRiskFeedback,
  queryDocumentQA,
  simplifyText
} from '../services/api';
import { 
  Scale, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  ShieldAlert, 
  Download, 
  FileText, 
  Send, 
  Languages, 
  ThumbsUp, 
  ThumbsDown,
  X,
  Sparkles
} from 'lucide-react';

interface DocumentWorkspaceProps {
  document: DocumentDetail;
  onClose: () => void;
  language: string;
}

export const DocumentWorkspace: React.FC<DocumentWorkspaceProps> = ({ document, onClose, language }) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'risks' | 'obligations' | 'compliance' | 'chat'>('risks');
  const [clauses, setClauses] = useState<ClauseItem[]>([]);
  const [risks, setRisks] = useState<RiskItem[]>([]);
  const [obligations, setObligations] = useState<ObligationItem[]>([]);
  const [compliance, setCompliance] = useState<ComplianceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedClauseId, setSelectedClauseId] = useState<number | null>(null);

  // Chat State
  const [chatMessages, setChatMessages] = useState<Array<{ sender: 'user' | 'ai'; text: string; citations?: string[]; page?: number }>>([
    {
      sender: 'ai',
      text: `Hello! I have indexed all ${document.page_count} pages of "${document.title}". Ask me any question regarding liabilities, obligations, termination conditions, or Indian law compliance.`
    }
  ]);
  const [chatInput, setChatInput] = useState('');
  const [isChatThinking, setIsChatThinking] = useState(false);

  // Risk filter
  const [riskSeverityFilter, setRiskSeverityFilter] = useState<string>('ALL');

  useEffect(() => {
    async function loadWorkspaceData() {
      setLoading(true);
      try {
        const [cData, rData, oData, compData] = await Promise.all([
          fetchDocumentClauses(document.id),
          fetchDocumentRisks(document.id),
          fetchDocumentObligations(document.id),
          fetchDocumentCompliance(document.id)
        ]);
        setClauses(cData);
        setRisks(rData);
        setObligations(oData);
        setCompliance(compData);
      } catch (err) {
        console.error('Failed to load workspace data', err);
      } finally {
        setLoading(false);
      }
    }
    loadWorkspaceData();
  }, [document.id]);

  const handleFeedback = async (riskId: number, fb: string) => {
    try {
      await submitRiskFeedback(riskId, fb);
      setRisks(prev => prev.map(r => r.id === riskId ? { ...r, user_feedback: fb } : r));
    } catch (e) {
      console.error(e);
    }
  };

  const handleSendChat = async () => {
    if (!chatInput.trim() || isChatThinking) return;
    const q = chatInput;
    setChatInput('');
    setChatMessages(prev => [...prev, { sender: 'user', text: q }]);
    setIsChatThinking(true);

    try {
      const res = await queryDocumentQA(document.id, q, language);
      setChatMessages(prev => [
        ...prev,
        {
          sender: 'ai',
          text: res.answer,
          citations: res.clause_citations,
          page: res.page_references?.[0]
        }
      ]);
    } catch (err) {
      setChatMessages(prev => [
        ...prev,
        { sender: 'ai', text: 'Error retrieving answer from document knowledge base.' }
      ]);
    } finally {
      setIsChatThinking(false);
    }
  };

  const filteredRisks = risks.filter(r => {
    if (riskSeverityFilter === 'ALL') return true;
    return r.severity.toUpperCase() === riskSeverityFilter;
  });

  const partiesList = (() => {
    try {
      return JSON.parse(document.parties_json);
    } catch {
      return [];
    }
  })();

  return (
    <div className="fixed inset-0 z-50 bg-[#0B0F19] flex flex-col overflow-hidden">
      {/* Workspace Top Bar */}
      <div className="h-16 border-b border-white/10 px-6 flex items-center justify-between bg-[#111827]">
        <div className="flex items-center space-x-4">
          <button 
            onClick={onClose}
            className="p-2 rounded-lg bg-white/5 hover:bg-white/10 text-slate-300 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              {document.title}
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-purple-500/20 text-purple-300 font-mono">
                {document.doc_type}
              </span>
            </h2>
            <div className="text-xs text-slate-400">
              {document.page_count} Pages • Governing Law: {document.governing_law} • Jurisdiction: {document.jurisdiction}
            </div>
          </div>
        </div>

        {/* Action Controls: Download PDF & Markdown */}
        <div className="flex items-center space-x-3">
          <a
            href={`/api/v1/reports/pdf/${document.id}`}
            download
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded-xl bg-[#1C253D] hover:bg-[#253252] border border-purple-500/30 text-purple-300 text-xs font-semibold transition-all shadow-sm"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Audit PDF</span>
          </a>
          <a
            href={`/api/v1/reports/markdown/${document.id}`}
            download
            className="flex items-center space-x-2 px-3.5 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 text-slate-300 text-xs font-semibold transition-all"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Export Brief (.md)</span>
          </a>
        </div>
      </div>

      {/* Two-Panel Body Layout */}
      <div className="flex-1 flex overflow-hidden">
        {/* LEFT PANEL: Original Document Viewer */}
        <div className="w-1/2 border-r border-white/10 flex flex-col bg-[#0D121F]">
          <div className="p-4 border-b border-white/5 flex items-center justify-between bg-[#101728]">
            <span className="text-xs font-bold text-slate-400 tracking-wider uppercase">
              Original Document Structure
            </span>
            <span className="text-xs text-slate-500">
              {clauses.length} Segmented Clauses
            </span>
          </div>

          <div className="flex-1 overflow-y-auto p-6 space-y-4">
            {loading ? (
              <div className="py-20 text-center text-slate-500">Loading document clauses...</div>
            ) : clauses.length > 0 ? (
              clauses.map((clause) => {
                const hasRisk = risks.some(r => r.clause_reference.toLowerCase() === clause.clause_number.toLowerCase() || clause.text.includes(r.clause_reference));
                const isSelected = selectedClauseId === clause.id;

                return (
                  <div
                    key={clause.id}
                    id={`clause-${clause.id}`}
                    onClick={() => setSelectedClauseId(clause.id)}
                    className={`p-4 rounded-xl border transition-all duration-200 cursor-pointer ${
                      isSelected
                        ? 'bg-[#1C2540] border-purple-500/60 shadow-lg'
                        : hasRisk
                        ? 'bg-[#181D2E] border-amber-500/30 hover:border-amber-500/60'
                        : 'bg-[#111726] border-white/5 hover:border-white/10'
                    }`}
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold text-purple-400 font-mono">
                          {clause.clause_number}
                        </span>
                        <span className="text-xs font-semibold text-slate-300">
                          {clause.heading}
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {hasRisk && (
                          <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300 flex items-center gap-1">
                            <AlertTriangle className="w-3 h-3" /> Risk Flagged
                          </span>
                        )}
                        <span className="text-[11px] text-slate-500 font-mono">
                          Page {clause.page_number}
                        </span>
                      </div>
                    </div>
                    <div className="text-xs text-slate-300 leading-relaxed font-mono whitespace-pre-wrap">
                      {clause.text}
                    </div>
                  </div>
                );
              })
            ) : (
              <div className="text-xs text-slate-300 whitespace-pre-wrap p-4 bg-[#111726] rounded-xl">
                {document.raw_text}
              </div>
            )}
          </div>
        </div>

        {/* RIGHT PANEL: AI Inspector & Intelligence Modules */}
        <div className="w-1/2 flex flex-col bg-[#111827]">
          {/* Tabs Navigation */}
          <div className="flex border-b border-white/10 bg-[#0E1524] px-4">
            {[
              { id: 'risks', label: 'Clause Risks', count: risks.length, icon: Scale },
              { id: 'obligations', label: 'Obligations & Deadlines', count: obligations.length, icon: Clock },
              { id: 'compliance', label: 'Statutory Compliance', count: compliance.length, icon: ShieldAlert },
              { id: 'overview', label: 'Entity Summary', icon: CheckCircle2 },
              { id: 'chat', label: 'Legal AI Chat', icon: Sparkles }
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`flex items-center space-x-2 px-4 py-3.5 text-xs font-bold transition-all border-b-2 ${
                    isActive
                      ? 'border-purple-500 text-purple-300 bg-[#162036]'
                      : 'border-transparent text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                  {tab.count !== undefined && (
                    <span className="px-1.5 py-0.2 rounded-full bg-slate-800 text-[10px] text-slate-400 font-mono">
                      {tab.count}
                    </span>
                  )}
                </button>
              );
            })}
          </div>

          {/* Tab Content Panel */}
          <div className="flex-1 overflow-y-auto p-6">
            {/* TAB 1: CLAUSE RISKS */}
            {activeTab === 'risks' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between pb-2 border-b border-white/5">
                  <div className="text-xs font-bold text-slate-400 uppercase">
                    Risk Breakdown ({filteredRisks.length} flagged)
                  </div>
                  <div className="flex space-x-1.5">
                    {['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'].map((lvl) => (
                      <button
                        key={lvl}
                        onClick={() => setRiskSeverityFilter(lvl)}
                        className={`px-2.5 py-1 rounded-lg text-[10px] font-bold tracking-wider transition-colors ${
                          riskSeverityFilter === lvl
                            ? 'bg-purple-600 text-white'
                            : 'bg-slate-800 text-slate-400 hover:text-white'
                        }`}
                      >
                        {lvl}
                      </button>
                    ))}
                  </div>
                </div>

                {filteredRisks.map((risk) => (
                  <div
                    key={risk.id}
                    className="p-5 rounded-2xl bg-[#141C2E] border border-white/5 hover:border-purple-500/30 transition-all space-y-3"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <span
                          className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                            risk.severity === 'Critical'
                              ? 'bg-red-950/80 border border-red-500/40 text-red-400'
                              : risk.severity === 'High'
                              ? 'bg-amber-950/80 border border-amber-500/40 text-amber-400'
                              : 'bg-blue-950/80 border border-blue-500/40 text-blue-400'
                          }`}
                        >
                          {risk.severity} Severity
                        </span>
                        <span className="text-xs font-bold text-white tracking-wide">
                          {risk.title}
                        </span>
                      </div>
                      <span className="text-xs font-bold text-purple-400 font-mono">
                        {Math.round(risk.confidence * 100)}% Confidence
                      </span>
                    </div>

                    <div className="text-xs text-slate-300 leading-relaxed bg-[#0F1524] p-3 rounded-xl border border-white/5">
                      <span className="font-semibold text-purple-300">Hazard Analysis: </span>
                      {risk.explanation}
                    </div>

                    <div className="text-xs text-emerald-300 leading-relaxed bg-[#0D1F17] p-3 rounded-xl border border-emerald-500/20">
                      <span className="font-semibold text-emerald-400">💡 Recommended Counter-Clause: </span>
                      {risk.remediation}
                    </div>

                    <div className="flex items-center justify-between pt-1 text-xs text-slate-400">
                      <div className="flex items-center gap-2">
                        <span>Source: <strong className="text-slate-200">{risk.clause_reference}</strong></span>
                        <span>•</span>
                        <span>Page {risk.page_number}</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-[11px] text-slate-500">Model Accuracy Feedback:</span>
                        <button
                          onClick={() => handleFeedback(risk.id, 'agree')}
                          className={`p-1 rounded hover:bg-white/10 ${risk.user_feedback === 'agree' ? 'text-emerald-400' : 'text-slate-400'}`}
                          title="Agree with risk finding"
                        >
                          <ThumbsUp className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleFeedback(risk.id, 'disagree')}
                          className={`p-1 rounded hover:bg-white/10 ${risk.user_feedback === 'disagree' ? 'text-red-400' : 'text-slate-400'}`}
                          title="Flag false positive"
                        >
                          <ThumbsDown className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* TAB 2: OBLIGATIONS & TIMELINE */}
            {activeTab === 'obligations' && (
              <div className="space-y-4">
                <div className="text-xs font-bold text-slate-400 uppercase pb-2 border-b border-white/5">
                  Chronological Obligations & Reminders
                </div>

                {obligations.map((ob, idx) => (
                  <div
                    key={ob.id || idx}
                    className="p-4 rounded-xl bg-[#141C2E] border border-white/5 space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <span className="px-2.5 py-0.5 rounded text-[10px] font-bold bg-purple-500/20 text-purple-300 uppercase">
                        {ob.category}
                      </span>
                      <span className={`text-xs font-semibold ${ob.is_ambiguous ? 'text-amber-400' : 'text-emerald-400'}`}>
                        {ob.deadline_text}
                      </span>
                    </div>

                    <div className="text-sm font-semibold text-white">
                      {ob.action}
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-xs text-slate-400 pt-1">
                      <div>Responsible: <strong className="text-slate-200">{ob.responsible_party}</strong></div>
                      <div>Amount: <strong className="text-slate-200">{ob.amount}</strong></div>
                      <div>Clause: <strong className="text-slate-200">{ob.clause_reference}</strong></div>
                      <div>Page: <strong className="text-slate-200">{ob.page_number}</strong></div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* TAB 3: STATUTORY COMPLIANCE */}
            {activeTab === 'compliance' && (
              <div className="space-y-4">
                <div className="text-xs font-bold text-slate-400 uppercase pb-2 border-b border-white/5">
                  Indian Statutory Checklist & Missing Clauses
                </div>

                {compliance.map((comp) => {
                  const isViolation = comp.status === 'Violation';
                  const isMissing = comp.status === 'Missing Clause';
                  const isCompliant = comp.status === 'Compliant';

                  return (
                    <div
                      key={comp.id}
                      className="p-4 rounded-xl bg-[#141C2E] border border-white/5 space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-xs font-bold text-white">
                            {comp.statute_name}
                          </div>
                          <div className="text-[11px] text-purple-400 font-mono">
                            {comp.section_reference}
                          </div>
                        </div>

                        <span
                          className={`px-2.5 py-1 rounded text-xs font-bold ${
                            isViolation
                              ? 'bg-red-950/80 border border-red-500/40 text-red-400'
                              : isMissing
                              ? 'bg-purple-950/80 border border-purple-500/40 text-purple-300'
                              : isCompliant
                              ? 'bg-emerald-950/80 border border-emerald-500/40 text-emerald-400'
                              : 'bg-slate-800 text-slate-300'
                          }`}
                        >
                          {comp.status}
                        </span>
                      </div>

                      <div className="text-xs text-slate-300 leading-relaxed bg-[#0F1524] p-3 rounded-lg">
                        {comp.details}
                      </div>

                      <div className="flex justify-end pt-1">
                        <a
                          href={comp.source_url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-[11px] text-purple-400 hover:underline"
                        >
                          View Official India Code / Gazette Reference →
                        </a>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}

            {/* TAB 4: ENTITY & OVERVIEW */}
            {activeTab === 'overview' && (
              <div className="space-y-5">
                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5 space-y-3">
                  <h3 className="text-xs font-bold text-slate-400 uppercase">Document Metadata</h3>
                  <div className="grid grid-cols-2 gap-3 text-xs">
                    <div>
                      <div className="text-slate-500">Document Type</div>
                      <div className="text-white font-semibold">{document.doc_type}</div>
                    </div>
                    <div>
                      <div className="text-slate-500">Classification Confidence</div>
                      <div className="text-purple-400 font-bold font-mono">
                        {Math.round(document.classification_confidence * 100)}%
                      </div>
                    </div>
                    <div>
                      <div className="text-slate-500">Effective Date</div>
                      <div className="text-white font-semibold">{document.effective_date}</div>
                    </div>
                    <div>
                      <div className="text-slate-500">Governing Law</div>
                      <div className="text-white font-semibold">{document.governing_law}</div>
                    </div>
                    <div className="col-span-2">
                      <div className="text-slate-500">Jurisdiction & Forum</div>
                      <div className="text-white font-semibold">{document.jurisdiction}</div>
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5 space-y-3">
                  <h3 className="text-xs font-bold text-slate-400 uppercase">Identified Parties</h3>
                  <div className="space-y-2">
                    {partiesList.map((p: string, idx: number) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-[#0F1524] text-xs font-semibold text-slate-200">
                        🏛️ {p}
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* TAB 5: LEGAL AI CHAT */}
            {activeTab === 'chat' && (
              <div className="h-full flex flex-col justify-between">
                <div className="space-y-3 mb-4 max-h-[460px] overflow-y-auto pr-2">
                  {chatMessages.map((msg, i) => (
                    <div
                      key={i}
                      className={`p-3.5 rounded-xl text-xs leading-relaxed ${
                        msg.sender === 'user'
                          ? 'bg-purple-900/30 border border-purple-500/30 text-purple-100 ml-8'
                          : 'bg-[#141C2E] border border-white/5 text-slate-200 mr-8'
                      }`}
                    >
                      <div className="font-bold text-[10px] text-slate-400 mb-1">
                        {msg.sender === 'user' ? 'YOU' : 'NYAYALENS AI ASSISTANT'}
                      </div>
                      <div className="whitespace-pre-wrap">{msg.text}</div>
                      {msg.citations && msg.citations.length > 0 && (
                        <div className="mt-2 pt-2 border-t border-white/10 text-[10px] text-purple-400 flex items-center gap-2">
                          <span>Evidence Citations: {msg.citations.join(', ')}</span>
                          {msg.page && <span>(Page {msg.page})</span>}
                        </div>
                      )}
                    </div>
                  ))}
                  {isChatThinking && (
                    <div className="p-3 rounded-xl bg-[#141C2E] text-xs text-purple-300 animate-pulse">
                      Analyzing semantic vector embeddings & searching clauses...
                    </div>
                  )}
                </div>

                <div className="flex items-center space-x-2 pt-2 border-t border-white/10">
                  <input
                    type="text"
                    value={chatInput}
                    onChange={(e) => setChatInput(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                    placeholder="Ask a question about this document..."
                    className="flex-1 bg-[#141C2E] border border-white/10 rounded-xl px-4 py-2.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-purple-500/50"
                  />
                  <button
                    onClick={handleSendChat}
                    className="p-2.5 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-medium text-xs transition-colors"
                  >
                    <Send className="w-4 h-4" />
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
