import React from 'react';
import { Clock, ArrowUpRight, ArrowDownLeft, DollarSign } from 'lucide-react';

export default function ActivitiesList({ activities }) {
  if (!activities || activities.length === 0) return null;

  return (
    <div className="glass-card p-6 rounded-2xl mb-6">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <Clock className="w-5 h-5 text-indigo-400" />
            Recent Activity & Transactions
          </h3>
          <p className="text-xs text-slate-400">Synced via SnapTrade Activities API</p>
        </div>
      </div>

      <div className="space-y-3">
        {activities.map((act) => {
          const isDepositOrDiv = act.type === 'DEPOSIT' || act.type === 'DIVIDEND' || act.type === 'SELL';
          return (
            <div key={act.id} className="flex items-center justify-between p-3.5 bg-slate-900/40 rounded-xl border border-slate-800/60 hover:border-slate-700/80 transition text-xs">
              <div className="flex items-center gap-3">
                <div className={`p-2.5 rounded-xl border ${isDepositOrDiv ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' : 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'}`}>
                  {isDepositOrDiv ? <ArrowDownLeft className="w-4 h-4" /> : <ArrowUpRight className="w-4 h-4" />}
                </div>
                <div>
                  <div className="font-bold text-slate-200 flex items-center gap-2">
                    <span>{act.type} {act.symbol}</span>
                    <span className="text-[10px] text-slate-400 font-normal px-2 py-0.5 bg-slate-800 rounded">
                      {act.date ? act.date.substring(0, 10) : 'Recent'}
                    </span>
                  </div>
                  <p className="text-slate-400 text-[11px] mt-0.5">{act.description}</p>
                </div>
              </div>

              <div className="text-right">
                <div className={`font-bold text-sm ${isDepositOrDiv ? 'text-emerald-400' : 'text-slate-200'}`}>
                  {isDepositOrDiv ? '+' : ''}${Math.abs(act.amount)?.toFixed(2)}
                </div>
                {act.units > 0 && <p className="text-[11px] text-slate-400">{act.units} shares</p>}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
