import React from 'react';
import { DollarSign, Wallet, TrendingUp, TrendingDown, PieChart, ShieldAlert } from 'lucide-react';

export default function PortfolioSummary({ summary, concentration }) {
  if (!summary) return null;

  const isPositive = summary.total_unrealized_pnl >= 0;

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {/* Total Net Worth */}
      <div className="glass-card glass-card-hover p-5 rounded-2xl relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400">Total Net Worth</span>
          <div className="p-2.5 bg-indigo-500/10 text-indigo-400 rounded-xl border border-indigo-500/20">
            <DollarSign className="w-5 h-5" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-50 tracking-tight mb-1">
          ${summary.total_portfolio_value?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
        </div>
        <p className="text-xs text-slate-400">Synced across {summary.accounts_count} brokerage accounts</p>
      </div>

      {/* Cash Balance */}
      <div className="glass-card glass-card-hover p-5 rounded-2xl relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400">Liquid Cash</span>
          <div className="p-2.5 bg-emerald-500/10 text-emerald-400 rounded-xl border border-emerald-500/20">
            <Wallet className="w-5 h-5" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-50 tracking-tight mb-1">
          ${summary.total_cash?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
        </div>
        <p className="text-xs text-emerald-400/80 font-medium">
          {((summary.total_cash / summary.total_portfolio_value) * 100).toFixed(1)}% of total portfolio
        </p>
      </div>

      {/* Total Gain / Loss */}
      <div className="glass-card glass-card-hover p-5 rounded-2xl relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400">Unrealized P&L</span>
          <div className={`p-2.5 rounded-xl border ${isPositive ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border-rose-500/20'}`}>
            {isPositive ? <TrendingUp className="w-5 h-5" /> : <TrendingDown className="w-5 h-5" />}
          </div>
        </div>
        <div className={`text-2xl font-bold tracking-tight mb-1 ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
          {isPositive ? '+' : ''}${summary.total_unrealized_pnl?.toLocaleString(undefined, { minimumFractionDigits: 2 })}
        </div>
        <p className={`text-xs font-semibold ${isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
          {isPositive ? '▲' : '▼'} {summary.total_pnl_percent}% overall return
        </p>
      </div>

      {/* Concentration Risk */}
      <div className="glass-card glass-card-hover p-5 rounded-2xl relative overflow-hidden">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-medium uppercase tracking-wider text-slate-400">Top 3 Concentration</span>
          <div className="p-2.5 bg-purple-500/10 text-purple-400 rounded-xl border border-purple-500/20">
            <PieChart className="w-5 h-5" />
          </div>
        </div>
        <div className="text-2xl font-bold text-slate-50 tracking-tight mb-1">
          {concentration?.top_3_concentration_pct}%
        </div>
        <div className="flex items-center gap-1.5 text-xs">
          <ShieldAlert className="w-3.5 h-3.5 text-amber-400" />
          <span className="text-slate-400">Risk Profile:</span>
          <span className="font-semibold text-amber-300">{concentration?.risk_level}</span>
        </div>
      </div>
    </div>
  );
}
