import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Sparkles, RefreshCw, Plus, AlertCircle, ChevronRight, CheckCircle2 } from 'lucide-react';
import ConnectionBanner from './components/ConnectionBanner';
import PortfolioSummary from './components/PortfolioSummary';
import AllocationCharts from './components/AllocationCharts';
import HoldingsTable from './components/HoldingsTable';
import ActivitiesList from './components/ActivitiesList';
import CopilotChatDrawer from './components/CopilotChatDrawer';
import ConnectModal from './components/ConnectModal';
import TopMovers from './components/TopMovers';
import RiskScoreCard from './components/RiskScoreCard';
import PnLWaterfallChart from './components/PnLWaterfallChart';
import ConcentrationRisk from './components/ConcentrationRisk';
import PortfolioHealthScore from './components/PortfolioHealthScore';

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isCopilotOpen, setIsCopilotOpen] = useState(false);
  const [isConnectOpen, setIsConnectOpen] = useState(false);
  const [lastRefresh, setLastRefresh] = useState(null);
  const [connectSuccessToast, setConnectSuccessToast] = useState(false);

  const fetchPortfolioData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await axios.get('/api/portfolio/overview?user_id=demo_user&user_secret=mock_secret_demo_user');
      setData(res.data);
      setLastRefresh(new Date());
    } catch (err) {
      console.error(err);
      setError('Unable to connect to backend portfolio service.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolioData();
    const params = new URLSearchParams(window.location.search);
    if (params.get('connected') === 'true') {
      setConnectSuccessToast(true);
      setTimeout(() => setConnectSuccessToast(false), 6000);
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);


  const handleAnalyzeWithAI = () => {
    setIsCopilotOpen(true);
  };

  return (
    <div className="min-h-screen text-slate-100 flex flex-col pb-20">
      {/* Top Navigation Bar */}
      <header className="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/80 px-6 py-4">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500 p-0.5 shadow-lg shadow-indigo-500/20">
              <div className="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center">
                <Sparkles className="w-5 h-5 text-indigo-400" />
              </div>
            </div>
            <div>
              <h1 className="font-extrabold text-lg text-slate-100 tracking-tight flex items-center gap-2">
                FolioMind <span className="gradient-text font-black">AI</span>
              </h1>
              <p className="text-[11px] text-slate-400 font-medium">SnapTrade Investment Portfolio Copilot</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {lastRefresh && (
              <span className="text-[10px] text-slate-500 hidden sm:block">
                Updated {lastRefresh.toLocaleTimeString()}
              </span>
            )}
            <button
              onClick={fetchPortfolioData}
              disabled={loading}
              className="p-2 bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-400 hover:text-slate-200 rounded-xl transition cursor-pointer"
              title="Refresh data"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            </button>
            <button
              onClick={() => setIsConnectOpen(true)}
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 border border-slate-700/80 text-slate-200 text-xs font-semibold rounded-xl transition flex items-center gap-2 cursor-pointer shadow-sm"
            >
              <Plus className="w-4 h-4 text-indigo-400" />
              Connect Brokerage
            </button>
            <button
              onClick={() => setIsCopilotOpen(true)}
              className="px-4 py-2 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white text-xs font-semibold rounded-xl transition flex items-center gap-2 shadow-lg shadow-indigo-600/30 cursor-pointer"
            >
              <Sparkles className="w-4 h-4" />
              AI Copilot
            </button>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 pt-6 flex-1 w-full">
        {/* Post-OAuth Connection Success Banner */}
        {connectSuccessToast && (
          <div className="mb-4 p-4 bg-emerald-500/15 border border-emerald-500/40 rounded-2xl flex items-center justify-between text-emerald-200 text-xs shadow-lg shadow-emerald-950/40">
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
              <span>
                <strong className="font-semibold text-emerald-100">Brokerage Connected Successfully!</strong> Your live portfolio and balances have been synced via SnapTrade.
              </span>
            </div>
            <button
              onClick={() => setConnectSuccessToast(false)}
              className="text-emerald-400 hover:text-emerald-200 font-bold ml-4 cursor-pointer"
            >
              ✕
            </button>
          </div>
        )}

        {/* Connection Status & Re-auth Alerts */}
        {data && (
          <ConnectionBanner
            connectionStatus={data.connection_status}
            onReconnect={() => setIsConnectOpen(true)}
          />
        )}


        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 space-y-4">
            <div className="w-12 h-12 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 animate-spin" />
            <p className="text-sm text-slate-400 font-medium">Syncing brokerage data via SnapTrade REST APIs...</p>
          </div>
        ) : error ? (
          <div className="glass-card p-8 rounded-3xl text-center max-w-lg mx-auto my-12 border-rose-500/30">
            <AlertCircle className="w-12 h-12 text-rose-400 mx-auto mb-3" />
            <h3 className="text-lg font-bold text-slate-100 mb-1">Backend Service Error</h3>
            <p className="text-xs text-slate-400 mb-6">{error}</p>
            <button
              onClick={fetchPortfolioData}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold text-xs rounded-xl transition cursor-pointer"
            >
              Retry Connection
            </button>
          </div>
        ) : data ? (
          <>
            {/* ── Row 1: Summary KPI Cards ── */}
            <PortfolioSummary summary={data.summary} concentration={data.concentration} />

            {/* ── Row 2: Health Score + Risk Profile (side by side) ── */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
              <PortfolioHealthScore health={data.health} />
              <RiskScoreCard riskMetrics={data.risk_metrics} />
            </div>

            {/* ── Row 3: P&L Contribution Waterfall (full width) ── */}
            <PnLWaterfallChart pnlWaterfall={data.pnl_waterfall} />

            {/* ── Row 4: Top Movers (full width) ── */}
            <TopMovers performers={data.performers} />

            {/* ── Row 5: Allocation Charts (full width) ── */}
            <AllocationCharts allocation={data.allocation} />

            {/* ── Row 6: Concentration Risk + Holdings Table ── */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
              <div className="lg:col-span-5">
                <ConcentrationRisk concentration={data.concentration} />
                <ActivitiesList activities={data.activities} />
              </div>
              <div className="lg:col-span-7">
                <HoldingsTable positions={data.positions} />
              </div>
            </div>

            {/* ── AI Analysis CTA Banner ── */}
            <div
              onClick={handleAnalyzeWithAI}
              className="w-full mb-8 p-5 rounded-2xl bg-gradient-to-r from-indigo-900/50 via-purple-900/40 to-pink-900/30 border border-indigo-500/20 cursor-pointer hover:border-indigo-400/40 transition group flex items-center justify-between"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                <div>
                  <p className="font-bold text-slate-100 text-sm">Get AI-Powered Portfolio Analysis</p>
                  <p className="text-xs text-slate-400">Ask FolioMind AI to explain your risk profile, top movers, and rebalancing opportunities</p>
                </div>
              </div>
              <ChevronRight className="w-5 h-5 text-indigo-400 group-hover:translate-x-1 transition-transform flex-shrink-0" />
            </div>
          </>
        ) : null}
      </main>

      {/* AI Copilot Side Drawer */}
      <CopilotChatDrawer isOpen={isCopilotOpen} onClose={() => setIsCopilotOpen(false)} />

      {/* Connect Modal */}
      <ConnectModal
        isOpen={isConnectOpen}
        onClose={() => setIsConnectOpen(false)}
        onConnected={fetchPortfolioData}
      />

      {/* Floating AI Copilot Action Button */}
      {!isCopilotOpen && (
        <button
          onClick={() => setIsCopilotOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-gradient-to-tr from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white rounded-2xl shadow-2xl shadow-indigo-600/50 flex items-center gap-2.5 font-semibold text-xs transition transform hover:scale-105 z-40 cursor-pointer border border-white/20"
        >
          <Sparkles className="w-5 h-5" />
          <span>Ask FolioMind AI</span>
        </button>
      )}
    </div>
  );
}
