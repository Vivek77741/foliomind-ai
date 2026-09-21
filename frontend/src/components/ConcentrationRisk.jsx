import React from 'react';
import { PieChart, AlertOctagon } from 'lucide-react';

export default function ConcentrationRisk({ concentration }) {
  if (!concentration) return null;
  const { top_holdings = [], top_3_concentration_pct = 0, risk_level } = concentration;

  const riskConfig = {
    High: { color: 'text-rose-400', bg: 'bg-rose-500/10', bar: 'bg-rose-500', label: 'High Concentration Risk' },
    Moderate: { color: 'text-amber-400', bg: 'bg-amber-500/10', bar: 'bg-amber-500', label: 'Moderate Concentration' },
    Low: { color: 'text-emerald-400', bg: 'bg-emerald-500/10', bar: 'bg-emerald-500', label: 'Well Distributed' },
  };
  const cfg = riskConfig[risk_level] || riskConfig.Moderate;

  return (
    <div className="glass-card p-6 rounded-2xl mb-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <PieChart className="w-5 h-5 text-indigo-400" />
          <div>
            <h3 className="text-lg font-bold text-slate-100">Position Concentration</h3>
            <p className="text-xs text-slate-400">Top 5 holdings by portfolio weight</p>
          </div>
        </div>
        <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider ${cfg.bg} ${cfg.color}`}>
          {cfg.label}
        </div>
      </div>

      {/* Top 3 Concentration Stat */}
      <div className="flex items-center gap-3 mb-5 p-3 bg-slate-900/60 rounded-xl border border-slate-800/50">
        <AlertOctagon className={`w-5 h-5 flex-shrink-0 ${cfg.color}`} />
        <div className="flex-1 min-w-0">
          <p className="text-xs text-slate-400">Top 3 positions hold</p>
          <div className="flex items-baseline gap-1">
            <span className={`text-2xl font-black ${cfg.color}`}>{top_3_concentration_pct}%</span>
            <span className="text-xs text-slate-500">of portfolio</span>
          </div>
        </div>
        <div className="w-24 text-right">
          <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${cfg.bar} transition-all duration-700`}
              style={{ width: `${Math.min(top_3_concentration_pct, 100)}%` }}
            />
          </div>
          <p className="text-[10px] text-slate-500 mt-1">Risk threshold: 60%</p>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="space-y-2">
        {top_holdings.map((h, i) => (
          <div key={h.symbol} className="flex items-center gap-3 group">
            <span className="text-xs text-slate-600 w-4 font-bold">#{i + 1}</span>
            <div className="flex-1 min-w-0">
              <div className="flex justify-between items-baseline mb-1">
                <span className="font-bold text-slate-200 text-xs">{h.symbol}</span>
                <span className="text-xs text-slate-400">{h.percentage}%</span>
              </div>
              <div className="h-1.5 bg-slate-800/80 rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700"
                  style={{
                    width: `${Math.min(h.percentage, 100)}%`,
                    background: `hsl(${220 + i * 30}, 70%, 60%)`
                  }}
                />
              </div>
            </div>
            <span className="text-xs text-slate-300 font-semibold w-20 text-right">
              ${h.market_value?.toLocaleString()}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
