import React, { useState } from 'react';
import { ShieldCheck, ArrowRight, X, Lock, CheckCircle2 } from 'lucide-react';
import axios from 'axios';

export default function ConnectModal({ isOpen, onClose, onConnected }) {
  const [loading, setLoading] = useState(false);
  const [useCustomKeys, setUseCustomKeys] = useState(false);
  const [clientId, setClientId] = useState('');
  const [consumerKey, setConsumerKey] = useState('');

  if (!isOpen) return null;

  const handleConnectSnapTrade = async () => {
    setLoading(true);
    try {
      // Call backend API to initiate login
      const res = await axios.post('/api/auth/login-url', {
        user_id: 'demo_user',
        user_secret: 'mock_secret_demo_user'
      });

      if (res.data.redirect_url) {
        if (res.data.is_demo) {
          // In demo sandbox mode, automatically refresh data
          onConnected();
          onClose();
        } else {
          // Redirect to real SnapTrade Connection Portal URL
          window.location.href = res.data.redirect_url;
        }
      }
    } catch (err) {
      alert("Failed to initiate SnapTrade connection. Falling back to Demo Sandbox.");
      onConnected();
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4">
      <div className="glass-card max-w-md w-full p-6 rounded-3xl border border-slate-700/60 shadow-2xl relative">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-200 rounded-xl transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="w-12 h-12 rounded-2xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 flex items-center justify-center mb-4">
          <ShieldCheck className="w-6 h-6" />
        </div>

        <h3 className="text-xl font-bold text-slate-100 mb-1">Connect Your Brokerage</h3>
        <p className="text-xs text-slate-400 mb-6 leading-relaxed">
          FolioMind uses <span className="text-slate-200 font-semibold">SnapTrade’s 256-bit OAuth portal</span>. Your login credentials are never visible to our servers.
        </p>

        <div className="space-y-3 mb-6 text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Supports 50+ brokerages (Alpaca, IBKR, Robinhood, Fidelity)</span>
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Read-only encrypted data pipeline via SnapTrade API</span>
          </div>
          <div className="flex items-center gap-2 text-slate-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Instant sync across multiple investment accounts</span>
          </div>
        </div>

        <button
          onClick={handleConnectSnapTrade}
          disabled={loading}
          className="w-full py-3.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-2xl transition shadow-lg shadow-indigo-600/30 flex items-center justify-center gap-2 text-sm cursor-pointer mb-3"
        >
          {loading ? "Redirecting to SnapTrade Portal..." : "Connect via SnapTrade OAuth"}
          <ArrowRight className="w-4 h-4" />
        </button>

        <p className="text-[11px] text-center text-slate-500 flex items-center justify-center gap-1">
          <Lock className="w-3 h-3" />
          Consumer secrets stay securely on backend
        </p>
      </div>
    </div>
  );
}
