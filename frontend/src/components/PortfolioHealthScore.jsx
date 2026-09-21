import React from 'react';
import { Activity } from 'lucide-react';

const gradeConfig = {
  A: { color: 'text-emerald-400', bg: 'bg-emerald-500/10', ring: 'ring-emerald-500/30' },
  B: { color: 'text-teal-400', bg: 'bg-teal-500/10', ring: 'ring-teal-500/30' },
  C: { color: 'text-amber-400', bg: 'bg-amber-500/10', ring: 'ring-amber-500/30' },
  D: { color: 'text-orange-400', bg: 'bg-orange-500/10', ring: 'ring-orange-500/30' },
  F: { color: 'text-rose-400', bg: 'bg-rose-500/10', ring: 'ring-rose-500/30' },
};

function ScoreBar({ score, max, color }) {
  const pct = (score / max) * 100;
  const barColor =
    pct >= 70 ? 'bg-emerald-500' : pct >= 45 ? 'bg-amber-500' : 'bg-rose-500';
  return (
    <div className="w-full bg-slate-800/60 rounded-full h-1.5 mt-1.5 overflow-hidden">
      <div
        className={`h-full rounded-full ${barColor} transition-all duration-700`}
        style={{ width: `${pct}%` }}
      />
    </div>
  );
}

export default function PortfolioHealthScore({ health }) {
  if (!health) return null;
  const { total_score, grade, label, breakdown } = health;
  const cfg = gradeConfig[grade] || gradeConfig['C'];

  return (
    <div className="glass-card p-6 rounded-2xl h-full">
      <div className="flex items-center gap-2 mb-5 pb-3 border-b border-slate-800">
        <Activity className="w-5 h-5 text-indigo-400" />
        <div>
          <h3 className="text-lg font-bold text-slate-100">Portfolio Health</h3>
          <p className="text-xs text-slate-400">Composite score across 4 dimensions</p>
        </div>
      </div>

      {/* Grade Badge + Total Score */}
      <div className="flex items-center gap-4 mb-6">
        <div className={`w-16 h-16 rounded-2xl ${cfg.bg} ring-2 ${cfg.ring} flex flex-col items-center justify-center flex-shrink-0`}>
          <span className={`text-3xl font-black ${cfg.color}`}>{grade}</span>
        </div>
        <div>
          <p className={`text-xl font-black ${cfg.color}`}>{total_score}<span className="text-sm text-slate-500 font-medium">/100</span></p>
          <p className="text-sm font-semibold text-slate-300">{label}</p>
          <p className="text-[11px] text-slate-500">Based on returns, risk & efficiency</p>
        </div>
      </div>

      {/* Breakdown */}
      <div className="space-y-3.5">
        {Object.entries(breakdown).map(([key, dim]) => (
          <div key={key}>
            <div className="flex justify-between items-baseline">
              <span className="text-xs text-slate-300 font-medium">{dim.label}</span>
              <span className="text-xs font-bold text-slate-100">{dim.score}<span className="text-slate-500">/{dim.max}</span></span>
            </div>
            <ScoreBar score={dim.score} max={dim.max} />
          </div>
        ))}
      </div>
    </div>
  );
}
