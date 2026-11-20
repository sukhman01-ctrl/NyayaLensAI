import React from 'react';
import { AIInsightItem } from '../types';

interface AiInsightsStreamProps {
  insights: AIInsightItem[];
  onInsightClick?: (insight: AIInsightItem) => void;
}

export const AiInsightsStream: React.FC<AiInsightsStreamProps> = ({ insights, onInsightClick }) => {
  return (
    <div className="bg-[#121929] border border-white/5 rounded-2xl p-6">
      <div className="flex items-center justify-between mb-5">
        <h2 className="text-sm font-bold tracking-wider text-slate-400 uppercase">
          AI Insights
        </h2>
        <span className="text-xs text-purple-400 font-medium">Real-time Stream</span>
      </div>

      <div className="space-y-4">
        {insights.map((item) => (
          <div
            key={item.id}
            onClick={() => onInsightClick && onInsightClick(item)}
            className="p-4 rounded-xl bg-[#0E1524] border border-white/5 hover:border-purple-500/30 transition-all duration-200 cursor-pointer"
          >
            {/* Title with icon */}
            <div className="text-xs font-bold tracking-wide text-slate-200 uppercase mb-2">
              {item.title}
            </div>

            {/* Description */}
            <div className="text-xs text-slate-400 leading-relaxed mb-3">
              {item.description}
            </div>

            {/* Confidence Progress Bar matching reference screenshot */}
            <div className="flex items-center space-x-3">
              <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-purple-600 to-indigo-500 rounded-full"
                  style={{ width: `${item.confidence}%` }}
                />
              </div>
              <span className="text-[11px] font-bold text-purple-300 font-mono">
                {item.confidence}%
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
