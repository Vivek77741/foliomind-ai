import React from 'react';
import { TrendingUp, TrendingDown, Award, AlertTriangle } from 'lucide-react';

export default function TopMovers({ performers }) {
  if (!performers) return null;
  const { gainers = [], decliners = [] } = performers;
  const top3Gainers = gainers.slice(0, 3);
  const top3Decliners = decliners.slice(0, 3);

  return (
    <div className="glass-card p-6 rounded-2xl mb-6">
      <div className="flex items-center gap-2 mb-5 pb-3 border-b border-slate-800">
        <Award className="w-5 h-5 text-indigo-400" />
        <div>
          <h3 className="text-lg font-bold text-slate-100">Top Movers</h3>
          <p className="text-xs text-slate-400">Best & worst performing positions by unrealized return</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Top Gainers */}
        <div>
          <p className="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5" /> Top Gainers
          </p>
          <div className="space-y-2.5">
            {top3Gainers.length === 0 && <p className="text-xs text-slate-500 italic">No gainers</p>}
            {top3Gainers.map((p, i) => (
              <div key={p.symbol} className="flex items-center justify-between p-3 bg-emerald-950/20 border border-emerald-500/15 rounded-xl">
                <div className="flex items-center gap-2.5">
                  <span className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 text-[10px] font-bold flex items-center justify-center">
                    #{i + 1}
                  </span>
                  <div>
                    <div className="font-bold text-slate-100 text-xs">{p.symbol}</div>
                    <div className="text-[10px] text-slate-400">{p.name}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-emerald-400 font-bold text-xs">+{p.unrealized_pnl_percent}%</div>
                  <div className="text-emerald-300 text-[10px]">+${p.unrealized_pnl?.toFixed(2)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Decliners */}
        <div>
          <p className="text-xs font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-1">
            <TrendingDown className="w-3.5 h-3.5" /> Decliners
          </p>
          <div className="space-y-2.5">
            {top3Decliners.length === 0 && <p className="text-xs text-slate-500 italic">No decliners today</p>}
            {top3Decliners.map((p, i) => (
              <div key={p.symbol} className="flex items-center justify-between p-3 bg-rose-950/20 border border-rose-500/15 rounded-xl">
                <div className="flex items-center gap-2.5">
                  <span className="w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 text-[10px] font-bold flex items-center justify-center">
                    #{i + 1}
                  </span>
                  <div>
                    <div className="font-bold text-slate-100 text-xs">{p.symbol}</div>
                    <div className="text-[10px] text-slate-400">{p.name}</div>
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-rose-400 font-bold text-xs">{p.unrealized_pnl_percent}%</div>
                  <div className="text-rose-300 text-[10px]">${p.unrealized_pnl?.toFixed(2)}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
