import React, { useState } from 'react';
import { X, GitCompare, AlertTriangle, CheckCircle2, ArrowRight } from 'lucide-react';
import { DocumentListItem, ComparisonResponse } from '../types';
import { compareDocuments } from '../services/api';

interface ComparisonModalProps {
  isOpen: boolean;
  onClose: () => void;
  documents: DocumentListItem[];
}

export const ComparisonModal: React.FC<ComparisonModalProps> = ({ isOpen, onClose, documents }) => {
  const [doc1Id, setDoc1Id] = useState<number>(documents[0]?.id || 1);
  const [doc2Id, setDoc2Id] = useState<number>(documents[1]?.id || (documents[0]?.id || 1));
  const [comparisonResult, setComparisonResult] = useState<ComparisonResponse | null>(null);
  const [isComparing, setIsComparing] = useState(false);

  if (!isOpen) return null;

  const handleRunComparison = async () => {
    if (doc1Id === doc2Id) {
      alert('Please select two different documents to compare.');
      return;
    }
    setIsComparing(true);
    try {
      const res = await compareDocuments(doc1Id, doc2Id);
      setComparisonResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsComparing(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-6">
      <div className="bg-[#101726] border border-white/10 rounded-2xl w-full max-w-5xl h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-white/10 flex items-center justify-between bg-[#131B2D]">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <GitCompare className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Cross-Document Comparison & Contradiction Detection</h3>
              <p className="text-xs text-slate-400">Semantic clause alignment, notice discrepancy checking, and change impact</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Document Selectors Bar */}
        <div className="p-4 bg-[#0E1524] border-b border-white/5 flex items-center justify-between gap-4">
          <div className="flex-1 flex items-center gap-3">
            <span className="text-xs font-bold text-slate-400 uppercase">Primary Draft:</span>
            <select
              value={doc1Id}
              onChange={(e) => setDoc1Id(Number(e.target.value))}
              className="flex-1 bg-[#162035] border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              {documents.map((d) => (
                <option key={d.id} value={d.id}>{d.title}</option>
              ))}
            </select>
          </div>

          <div className="text-slate-500">
            <ArrowRight className="w-4 h-4" />
          </div>

          <div className="flex-1 flex items-center gap-3">
            <span className="text-xs font-bold text-slate-400 uppercase">Revision / Addendum:</span>
            <select
              value={doc2Id}
              onChange={(e) => setDoc2Id(Number(e.target.value))}
              className="flex-1 bg-[#162035] border border-white/10 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              {documents.map((d) => (
                <option key={d.id} value={d.id}>{d.title}</option>
              ))}
            </select>
          </div>

          <button
            onClick={handleRunComparison}
            disabled={isComparing}
            className="px-5 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-semibold text-xs transition-colors shrink-0 disabled:opacity-50"
          >
            {isComparing ? 'Comparing...' : 'Run Semantic Diff'}
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {comparisonResult ? (
            <div className="space-y-4">
              <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5 flex items-center justify-between">
                <div className="text-xs text-slate-300">
                  {comparisonResult.summary}
                </div>
                <div className="flex gap-3">
                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300">
                    {comparisonResult.contradictions_count} Contradictions Flagged
                  </span>
                  <span className="px-3 py-1 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300">
                    {comparisonResult.total_modifications} Clauses Changed
                  </span>
                </div>
              </div>

              {comparisonResult.diff_items.map((diff, idx) => (
                <div
                  key={idx}
                  className={`p-5 rounded-2xl border space-y-3 ${
                    diff.is_contradiction
                      ? 'bg-[#1C141E] border-red-500/40'
                      : diff.change_type === 'MODIFIED'
                      ? 'bg-[#161F33] border-white/10'
                      : 'bg-[#121929] border-white/5'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span
                        className={`px-2.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                          diff.is_contradiction
                            ? 'bg-red-950 text-red-400 border border-red-500/40'
                            : diff.change_type === 'ADDED'
                            ? 'bg-emerald-950 text-emerald-400'
                            : diff.change_type === 'REMOVED'
                            ? 'bg-slate-800 text-slate-400'
                            : 'bg-blue-950 text-blue-400'
                        }`}
                      >
                        {diff.is_contradiction ? 'CONTRADICTION DETECTED' : diff.change_type}
                      </span>
                      <span className="text-xs font-bold text-white">
                        {diff.clause_title}
                      </span>
                    </div>
                  </div>

                  <div className="grid grid-cols-2 gap-4 text-xs font-mono">
                    <div className="p-3 rounded-xl bg-[#0D121D] border border-white/5">
                      <div className="text-slate-500 text-[10px] mb-1 uppercase">Doc 1: {comparisonResult.doc1_title}</div>
                      <div className="text-slate-300 whitespace-pre-wrap">{diff.doc1_text || '[Clause Not Present]'}</div>
                    </div>
                    <div className="p-3 rounded-xl bg-[#0D121D] border border-white/5">
                      <div className="text-slate-500 text-[10px] mb-1 uppercase">Doc 2: {comparisonResult.doc2_title}</div>
                      <div className="text-slate-300 whitespace-pre-wrap">{diff.doc2_text || '[Clause Removed]'}</div>
                    </div>
                  </div>

                  <div className="text-xs text-amber-300 bg-amber-950/20 p-2.5 rounded-lg border border-amber-500/20">
                    <strong>Practical Legal Impact: </strong>{diff.impact_explanation}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="py-24 text-center text-slate-500 text-sm">
              Select two documents above and click <strong>"Run Semantic Diff"</strong> to analyze clause modifications and contradictions.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
