import React from 'react';
import { ShieldCheck, RefreshCw, AlertTriangle, ExternalLink } from 'lucide-react';

export default function ConnectionBanner({ connectionStatus, onReconnect }) {
  if (!connectionStatus) return null;

  const { is_active, needs_reauth, brokerage_name, is_demo } = connectionStatus;

  return (
    <div className="w-full mb-6">
      {needs_reauth ? (
        <div className="glass-card border-amber-500/30 bg-amber-950/20 p-4 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-amber-500/10 text-amber-400 rounded-xl border border-amber-500/20">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <h4 className="font-semibold text-amber-200">Brokerage Re-authorization Required</h4>
              <p className="text-sm text-amber-400/80">
                Your connection to <span className="font-medium text-amber-200">{brokerage_name}</span> has expired or needs permissions refreshed.
              </p>
            </div>
          </div>
          <button
            onClick={onReconnect}
            className="flex items-center gap-2 px-4 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-semibold rounded-xl transition text-sm shadow-lg shadow-amber-500/20 cursor-pointer"
          >
            <RefreshCw className="w-4 h-4" />
            Reconnect Brokerage
          </button>
        </div>
      ) : (
        <div className="glass-card p-3 px-5 rounded-2xl flex flex-wrap items-center justify-between gap-3 text-xs md:text-sm">
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-2 px-3 py-1 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              Connected
            </div>
            <span className="text-slate-400">Brokerage:</span>
            <span className="font-semibold text-slate-200 flex items-center gap-1.5">
              {brokerage_name}
              {is_demo && (
                <span className="px-2 py-0.5 bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 rounded-md text-xs font-normal">
                  Demo Sandbox Mode
                </span>
              )}
            </span>
          </div>

          <div className="flex items-center gap-3 text-slate-400">
            <span className="flex items-center gap-1 text-slate-300">
              <ShieldCheck className="w-4 h-4 text-indigo-400" />
              SnapTrade 256-bit OAuth Sync
            </span>
            <button
              onClick={onReconnect}
              className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1 underline font-medium cursor-pointer"
            >
              Switch Connection <ExternalLink className="w-3 h-3" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
