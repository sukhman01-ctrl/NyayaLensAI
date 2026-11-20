import React from 'react';
import { 
  FileText, 
  Search, 
  Scale, 
  CheckSquare, 
  BarChart3, 
  Settings,
  GitCompare,
  ShieldCheck,
  MessageSquareText,
  Cpu
} from 'lucide-react';

interface SidebarProps {
  currentView: string;
  onSelectView: (view: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ currentView, onSelectView }) => {
  const navItems = [
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'contract_review', label: 'Contract Review', icon: Search },
    { id: 'risk_analysis', label: 'Risk Analysis', icon: Scale },
    { id: 'clause_extraction', label: 'Clause Extraction', icon: CheckSquare },
    { id: 'comparison', label: 'Doc Comparison', icon: GitCompare },
    { id: 'compliance', label: 'Compliance Audit', icon: ShieldCheck },
    { id: 'assistant', label: 'Legal AI Chat', icon: MessageSquareText },
    { id: 'evaluation', label: 'ML Evaluation Metrics', icon: Cpu },
    { id: 'reports', label: 'Reports', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 bg-[#0F1422] border-r border-white/5 flex flex-col justify-between shrink-0 min-h-screen">
      <div>
        {/* Brand Header matching reference screenshot */}
        <div className="p-6 flex items-center space-x-3 cursor-pointer" onClick={() => onSelectView('documents')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-brand-violet to-brand-purple flex items-center justify-center shadow-lg shadow-purple-500/20 font-bold text-white text-xl">
            L
          </div>
          <div>
            <div className="text-lg font-bold tracking-tight text-white flex items-center gap-1">
              LexAI <span className="text-[10px] bg-purple-500/20 text-purple-300 px-1.5 py-0.5 rounded font-mono">NyayaLens</span>
            </div>
            <div className="text-xs text-slate-400 font-medium">Legal Intelligence Platform</div>
          </div>
        </div>

        {/* Navigation list */}
        <nav className="px-3 space-y-1.5 mt-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = currentView === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectView(item.id)}
                className={`w-full flex items-center space-x-3.5 px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 ${
                  isActive
                    ? 'bg-[#1E2640] text-purple-300 font-semibold shadow-sm border border-purple-500/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-purple-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* System Status footer */}
      <div className="p-4 m-3 rounded-xl bg-[#141B2D] border border-white/5 text-xs">
        <div className="flex items-center justify-between text-slate-400 mb-1">
          <span>Engine Status</span>
          <span className="flex items-center gap-1.5 text-emerald-400 font-medium">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Online
          </span>
        </div>
        <div className="text-[11px] text-slate-500 truncate">
          v1.0 • Indian Statutory RAG v2026
        </div>
      </div>
    </aside>
  );
};
