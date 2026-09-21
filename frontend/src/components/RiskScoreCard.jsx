import React from 'react';
import { ShieldCheck, AlertTriangle, Zap } from 'lucide-react';

function RingGauge({ score, size = 120, strokeWidth = 10 }) {
  const radius = (size - strokeWidth) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  const color =
    score >= 70 ? '#10b981' : score >= 45 ? '#f59e0b' : '#f43f5e';

  return (
    <svg width={size} height={size} className="rotate-[-90deg]">
      <circle
        cx={size / 2} cy={size / 2} r={radius}
        fill="none" stroke="#1e293b" strokeWidth={strokeWidth}
      />
      <circle
        cx={size / 2} cy={size / 2} r={radius}
        fill="none" stroke={color} strokeWidth={strokeWidth}
        strokeDasharray={circumference}
        strokeDashoffset={offset}
        strokeLinecap="round"
        style={{ transition: 'stroke-dashoffset 1s ease' }}
      />
    </svg>
  );
}

export default function RiskScoreCard({ riskMetrics }) {
  if (!riskMetrics) return null;

  const {
    risk_score = 0, diversification_score = 0, cash_drag_pct = 0,
    dominant_sector = 'N/A', dominant_sector_pct = 0, risk_label, risk_color,
    hhi = 0, position_count = 0
  } = riskMetrics;

  const colorMap = {
    emerald: { text: 'text-emerald-400', bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
    amber: { text: 'text-amber-400', bg: 'bg-amber-500/10', border: 'border-amber-500/20' },
    rose: { text: 'text-rose-400', bg: 'bg-rose-500/10', border: 'border-rose-500/20' },
  };
  const colors = colorMap[risk_color] || colorMap.amber;

  const metrics = [
    { label: 'Diversification', value: `${diversification_score}/100`, sub: 'HHI-based score' },
    { label: 'Cash Drag', value: `${cash_drag_pct}%`, sub: 'Idle uninvested cash' },
    { label: 'Top Sector', value: dominant_sector, sub: `${dominant_sector_pct}% of portfolio` },
    { label: 'Positions', value: position_count, sub: 'Active holdings' },
  ];

  return (
    <div className="glass-card p-6 rounded-2xl h-full">
      <div className="flex items-center gap-2 mb-5 pb-3 border-b border-slate-800">
        <ShieldCheck className="w-5 h-5 text-indigo-400" />
        <div>
          <h3 className="text-lg font-bold text-slate-100">Risk Profile</h3>
          <p className="text-xs text-slate-400">Concentration & diversification analytics</p>
        </div>
      </div>

      {/* Ring Gauge + Score */}
      <div className="flex flex-col items-center mb-6">
        <div className="relative">
          <RingGauge score={risk_score} size={130} strokeWidth={12} />
          <div className="absolute inset-0 flex flex-col items-center justify-center rotate-0">
            <span className="text-3xl font-black text-slate-100">{risk_score}</span>
            <span className="text-[10px] text-slate-400 font-semibold">/100</span>
          </div>
        </div>
        <div className={`mt-2 px-3 py-1 rounded-full text-xs font-bold ${colors.bg} ${colors.text} ${colors.border} border`}>
          {risk_label}
        </div>
      </div>

      {/* Metric Grid */}
      <div className="grid grid-cols-2 gap-2.5">
        {metrics.map((m) => (
          <div key={m.label} className="bg-slate-900/60 rounded-xl p-3 border border-slate-800/50">
            <div className="text-slate-400 text-[10px] uppercase tracking-wider mb-1">{m.label}</div>
            <div className="font-bold text-slate-100 text-sm">{m.value}</div>
            <div className="text-[10px] text-slate-500">{m.sub}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
