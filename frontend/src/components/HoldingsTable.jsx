import React from 'react';
import { Briefcase, TrendingUp, TrendingDown } from 'lucide-react';

export default function HoldingsTable({ positions }) {
  if (!positions || positions.length === 0) return null;

  return (
    <div className="glass-card p-6 rounded-2xl mb-6 overflow-hidden">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Briefcase className="w-5 h-5 text-indigo-400" />
            Active Holdings & Positions
          </h3>
          <p className="text-xs text-slate-400">Live position details synced via SnapTrade API</p>
        </div>
        <span className="px-3 py-1 bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-xs font-semibold rounded-full">
          {positions.length} Active Asset{positions.length > 1 ? 's' : ''}
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="border-b border-slate-800 text-slate-400 font-semibold uppercase tracking-wider">
              <th className="py-3 px-4">Asset / Ticker</th>
              <th className="py-3 px-4">Sector</th>
              <th className="py-3 px-4 text-right">Shares</th>
              <th className="py-3 px-4 text-right">Avg Price</th>
              <th className="py-3 px-4 text-right">Current Price</th>
              <th className="py-3 px-4 text-right">Market Value</th>
              <th className="py-3 px-4 text-right">Unrealized P&L</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {positions.map((pos) => {
              const isPos = pos.unrealized_pnl >= 0;
              return (
                <tr key={pos.symbol} className="hover:bg-slate-900/40 transition">
                  <td className="py-3.5 px-4 font-semibold text-slate-100">
                    <div className="flex items-center gap-2.5">
                      <div className="w-8 h-8 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center font-bold text-xs">
                        {pos.symbol.substring(0, 3)}
                      </div>
                      <div>
                        <div className="font-bold text-slate-100">{pos.symbol}</div>
                        <div className="text-[11px] text-slate-400 font-normal">{pos.description}</div>
                      </div>
                    </div>
                  </td>
                  <td className="py-3.5 px-4">
                    <span className="px-2.5 py-1 bg-slate-900 text-slate-300 border border-slate-800 rounded-md font-medium">
                      {pos.sector}
                    </span>
                  </td>
                  <td className="py-3.5 px-4 text-right font-medium text-slate-200">{pos.units}</td>
                  <td className="py-3.5 px-4 text-right text-slate-400">${pos.open_price?.toFixed(2)}</td>
                  <td className="py-3.5 px-4 text-right font-semibold text-slate-200">${pos.price?.toFixed(2)}</td>
                  <td className="py-3.5 px-4 text-right font-bold text-slate-100">${pos.market_value?.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                  <td className="py-3.5 px-4 text-right">
                    <div className={`inline-flex items-center gap-1 font-bold ${isPos ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {isPos ? <TrendingUp className="w-3.5 h-3.5" /> : <TrendingDown className="w-3.5 h-3.5" />}
                      {isPos ? '+' : ''}${pos.unrealized_pnl?.toFixed(2)} ({isPos ? '+' : ''}{pos.unrealized_pnl_percent}%)
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
