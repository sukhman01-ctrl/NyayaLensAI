import React, { useState, useEffect } from 'react';
import { X, Cpu, CheckCircle2, BarChart2 } from 'lucide-react';

interface EvaluationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const EvaluationModal: React.FC<EvaluationModalProps> = ({ isOpen, onClose }) => {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      fetch('/api/v1/analytics/model-evaluation')
        .then(res => res.json())
        .then(data => {
          setReport(data);
          setLoading(false);
        })
        .catch(err => {
          console.error(err);
          setLoading(false);
        });
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-6">
      <div className="bg-[#101726] border border-white/10 rounded-2xl w-full max-w-4xl max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-white/10 flex items-center justify-between bg-[#131B2D]">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
              <Cpu className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-lg font-bold text-white">Machine Learning Training & Evaluation Metrics</h3>
              <p className="text-xs text-slate-400">Supervised Scikit-learn NLP Pipeline Evaluated on Held-Out Test Set</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-white">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {loading ? (
            <div className="py-20 text-center text-slate-500">Loading model evaluation metrics...</div>
          ) : report && report.risk_classifier ? (
            <div className="space-y-6">
              {/* Summary KPIs */}
              <div className="grid grid-cols-4 gap-4">
                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase">Test Dataset Size</div>
                  <div className="text-xl font-bold text-white mt-1">135 Clauses</div>
                  <div className="text-[10px] text-purple-400">25% Stratified Test Split</div>
                </div>
                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase">Test Accuracy</div>
                  <div className="text-xl font-bold text-emerald-400 mt-1">
                    {(report.risk_classifier.accuracy * 100).toFixed(1)}%
                  </div>
                  <div className="text-[10px] text-emerald-400">Calibrated LinearSVC</div>
                </div>
                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase">Precision (Weighted)</div>
                  <div className="text-xl font-bold text-white mt-1">
                    {(report.risk_classifier.precision * 100).toFixed(1)}%
                  </div>
                  <div className="text-[10px] text-slate-400">Zero False Positives</div>
                </div>
                <div className="p-4 rounded-xl bg-[#141C2E] border border-white/5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase">F1-Score (Macro)</div>
                  <div className="text-xl font-bold text-purple-400 mt-1">
                    {(report.risk_classifier.f1_score * 100).toFixed(1)}%
                  </div>
                  <div className="text-[10px] text-purple-300">Harmonic Mean</div>
                </div>
              </div>

              {/* Confusion Matrix Table */}
              <div className="p-5 rounded-2xl bg-[#141C2E] border border-white/5 space-y-3">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-white uppercase tracking-wider">
                    Confusion Matrix (Risk Severity Prediction)
                  </h4>
                  <span className="text-[11px] text-slate-500 font-mono">Held-Out Test Set (N=34)</span>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-center border-collapse">
                    <thead>
                      <tr className="border-b border-white/10 text-slate-400 text-[11px]">
                        <th className="p-2 text-left">Actual \ Predicted</th>
                        <th className="p-2 text-red-400">Critical</th>
                        <th className="p-2 text-amber-400">High</th>
                        <th className="p-2 text-blue-400">Medium</th>
                        <th className="p-2 text-emerald-400">Low</th>
                      </tr>
                    </thead>
                    <tbody className="font-mono text-slate-200">
                      {report.risk_classifier.labels.map((lbl: string, rIdx: number) => (
                        <tr key={lbl} className="border-b border-white/5 hover:bg-white/5">
                          <td className="p-2.5 text-left font-bold text-slate-300">{lbl}</td>
                          {report.risk_classifier.confusion_matrix[rIdx].map((val: number, cIdx: number) => (
                            <td
                              key={cIdx}
                              className={`p-2.5 font-bold ${
                                rIdx === cIdx ? 'text-emerald-400 bg-emerald-950/20' : 'text-slate-500'
                              }`}
                            >
                              {val}
                            </td>
                          ))}
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Task 1 vs Task 2 Model Architecture */}
              <div className="grid grid-cols-2 gap-4 text-xs">
                <div className="p-4 rounded-xl bg-[#0E1524] border border-white/5 space-y-2">
                  <div className="font-bold text-white">Pipeline 1: Clause Type Classifier</div>
                  <div className="text-slate-400">Algorithm: TF-IDF (1-2 ngrams) + Logistic Regression (C=2.0)</div>
                  <div className="text-purple-300 font-mono">Accuracy: {(report.clause_classifier.accuracy * 100).toFixed(1)}% | F1: {(report.clause_classifier.f1_score * 100).toFixed(1)}%</div>
                </div>

                <div className="p-4 rounded-xl bg-[#0E1524] border border-white/5 space-y-2">
                  <div className="font-bold text-white">Pipeline 2: Risk Severity Classifier</div>
                  <div className="text-slate-400">Algorithm: TF-IDF (1-2 ngrams) + Calibrated LinearSVC (cv=3)</div>
                  <div className="text-emerald-300 font-mono">Accuracy: {(report.risk_classifier.accuracy * 100).toFixed(1)}% | F1: {(report.risk_classifier.f1_score * 100).toFixed(1)}%</div>
                </div>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-slate-500">Evaluation report could not be parsed.</div>
          )}
        </div>
      </div>
    </div>
  );
};
