import React from 'react';
import { DashboardKPIs } from '../types';

interface MetricCardsProps {
  kpis: DashboardKPIs | null;
}

export const MetricCards: React.FC<MetricCardsProps> = ({ kpis }) => {
  const cards = [
    {
      label: 'DOCS ANALYZED',
      value: kpis?.docs_analyzed.value || '2,847',
      trend: kpis?.docs_analyzed.trend || '↑ 12% this month',
      trendColor: 'text-emerald-400'
    },
    {
      label: 'RISKS FLAGGED',
      value: kpis?.risks_flagged.value || '143',
      trend: kpis?.risks_flagged.trend || '↑ 8 this week',
      trendColor: 'text-amber-400'
    },
    {
      label: 'REVIEW TIME SAVED',
      value: kpis?.review_time_saved.value || '89%',
      trend: kpis?.review_time_saved.trend || 'vs. manual review',
      trendColor: 'text-emerald-400'
    },
    {
      label: 'AI ACCURACY',
      value: kpis?.ai_accuracy.value || '97.3%',
      trend: kpis?.ai_accuracy.trend || '↑ 1.2% this quarter',
      trendColor: 'text-emerald-400'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5 mb-8">
      {cards.map((card, idx) => (
        <div
          key={idx}
          className="bg-[#121929] border border-white/5 rounded-2xl p-6 shadow-md hover:border-purple-500/30 transition-all duration-200"
        >
          <div className="text-[11px] font-bold tracking-wider text-slate-400 uppercase mb-2">
            {card.label}
          </div>
          <div className="text-3xl font-extrabold text-white tracking-tight mb-2">
            {card.value}
          </div>
          <div className={`text-xs font-semibold ${card.trendColor}`}>
            {card.trend}
          </div>
        </div>
      ))}
    </div>
  );
};
