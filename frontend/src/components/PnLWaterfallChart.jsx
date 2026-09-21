import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine
} from 'recharts';
import { BarChart2 } from 'lucide-react';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const d = payload[0].payload;
    return (
      <div className="bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs shadow-xl">
        <p className="font-bold text-slate-100 mb-1">{d.symbol}</p>
        <p className={d.pnl >= 0 ? 'text-emerald-400' : 'text-rose-400'}>
          P&L: {d.pnl >= 0 ? '+' : ''}${d.pnl.toFixed(2)}
        </p>
        <p className={d.pnl >= 0 ? 'text-emerald-300' : 'text-rose-300'}>
          Return: {d.pnl_percent >= 0 ? '+' : ''}{d.pnl_percent}%
        </p>
      </div>
    );
  }
  return null;
};

export default function PnLWaterfallChart({ pnlWaterfall }) {
  if (!pnlWaterfall || pnlWaterfall.length === 0) return null;

  // Sort gainers first, then decliners for visual impact
  const sorted = [...pnlWaterfall].sort((a, b) => b.pnl - a.pnl);

  return (
    <div className="glass-card p-6 rounded-2xl mb-6">
      <div className="flex items-center justify-between mb-5 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <BarChart2 className="w-5 h-5 text-indigo-400" />
          <div>
            <h3 className="text-lg font-bold text-slate-100">P&L Contribution</h3>
            <p className="text-xs text-slate-400">Unrealized gain/loss by position (top 10)</p>
          </div>
        </div>
        <div className="flex items-center gap-3 text-xs">
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block" />
            <span className="text-slate-400">Gain</span>
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block" />
            <span className="text-slate-400">Loss</span>
          </span>
        </div>
      </div>

      <div className="h-56">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={sorted} margin={{ top: 4, right: 8, left: 8, bottom: 4 }} barSize={28}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis
              dataKey="symbol"
              tick={{ fill: '#94a3b8', fontSize: 11, fontWeight: 600 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={(v) => `$${v >= 0 ? '+' : ''}${v.toFixed(0)}`}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(99,102,241,0.08)' }} />
            <ReferenceLine y={0} stroke="#334155" strokeWidth={1.5} />
            <Bar dataKey="pnl" radius={[4, 4, 0, 0]}>
              {sorted.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.pnl >= 0 ? '#10b981' : '#f43f5e'}
                  fillOpacity={0.85}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
