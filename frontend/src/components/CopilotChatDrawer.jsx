import React, { useState, useRef, useEffect } from 'react';
import { Bot, Send, Sparkles, X, ChevronRight, Cpu, ShieldCheck } from 'lucide-react';
import axios from 'axios';

const PROMPT_CHIPS = [
  "NVDA",
  "Why did my portfolio change this week?",
  "What are my highest risk concentrations?",
  "How diversified am I across sectors?",
  "Show my cash & liquid balance summary"
];

// Helper to render basic markdown formatting cleanly
const FormattedMessage = ({ text }) => {
  if (!text) return null;

  const lines = text.split('\n');

  return (
    <div className="space-y-2 text-xs leading-relaxed">
      {lines.map((line, idx) => {
        const trimmed = line.trim();
        if (!trimmed) return <div key={idx} className="h-1" />;

        // Header lines starting with emojis or titles
        if (
          trimmed.startsWith('📊') ||
          trimmed.startsWith('🔍') ||
          trimmed.startsWith('💵') ||
          trimmed.startsWith('📜') ||
          trimmed.startsWith('🤖') ||
          trimmed.startsWith('📈') ||
          trimmed.startsWith('##') ||
          trimmed.startsWith('#')
        ) {
          const cleanHeader = trimmed.replace(/^#+\s*/, '').replace(/\*\*/g, '');
          return (
            <div key={idx} className="font-extrabold text-sm text-indigo-300 pb-1 flex items-center gap-1.5">
              {cleanHeader}
            </div>
          );
        }

        // Parse bold segments **text**
        const parts = line.split(/(\*\*.*?\*\*)/g);
        const formattedLine = parts.map((part, pIdx) => {
          if (part.startsWith('**') && part.endsWith('**')) {
            return (
              <strong key={pIdx} className="font-bold text-slate-50">
                {part.slice(2, -2)}
              </strong>
            );
          }
          return part;
        });

        // Bullet point lines
        if (trimmed.startsWith('•') || trimmed.startsWith('-') || trimmed.startsWith('*')) {
          return (
            <div key={idx} className="pl-3 relative border-l-2 border-indigo-500/40 py-0.5 text-slate-200">
              {formattedLine}
            </div>
          );
        }

        return <p key={idx} className="text-slate-200">{formattedLine}</p>;
      })}
    </div>
  );
};

export default function CopilotChatDrawer({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    {
      sender: 'agent',
      text: "👋 Hi! I'm **FolioMind AI**, your investment portfolio copilot.\n\nI analyze your live brokerage accounts connected via **SnapTrade**, run deterministic analytics, and provide 100% grounded explanations.\n\nAsk me anything like **'NVDA'**, **'Why did my portfolio change?'**, or **'Show risk breakdown'**!",
      tools: ["snaptrade_connect()", "fetch_balances()"]
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = { sender: 'user', text: query };
    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setLoading(true);

    try {
      const res = await axios.post('/api/copilot/chat', {
        query: query,
        user_id: 'demo_user',
        user_secret: 'mock_secret_demo_user'
      });

      const agentMsg = {
        sender: 'agent',
        text: res.data.response,
        tools: res.data.tools_executed || []
      };

      setMessages((prev) => [...prev, agentMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'agent',
          text: "⚠️ Sorry, I encountered an issue fetching portfolio analytics. Please try again.",
          tools: ["error_boundary()"]
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-full sm:w-[480px] glass-card border-l border-slate-700/60 z-50 flex flex-col shadow-2xl animate-in slide-in-from-right duration-300">
      {/* Header */}
      <div className="p-4 px-6 border-b border-slate-800 flex items-center justify-between bg-slate-950/90">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-600/30 text-white font-bold">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-slate-100 flex items-center gap-2 text-base">
              FolioMind AI Copilot
              <span className="px-2 py-0.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-[10px] rounded-full font-semibold">
                Grounded Mode
              </span>
            </h3>
            <p className="text-xs text-slate-400 flex items-center gap-1">
              <ShieldCheck className="w-3.5 h-3.5 text-indigo-400" />
              Powered by SnapTrade REST APIs
            </p>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-2 text-slate-400 hover:text-slate-200 hover:bg-slate-800 rounded-xl transition cursor-pointer"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex flex-col ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}
          >
            {msg.sender === 'agent' && (
              <div className="flex items-center gap-1.5 mb-1.5 text-[11px] font-semibold text-indigo-400">
                <Bot className="w-3.5 h-3.5" />
                FolioMind AI
              </div>
            )}

            <div
              className={`p-4 rounded-2xl max-w-[92%] text-xs leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-indigo-600 text-white rounded-br-none shadow-md shadow-indigo-600/20 font-semibold'
                  : 'glass-card bg-slate-900/95 text-slate-200 rounded-bl-none border-slate-700/60 shadow-lg'
              }`}
            >
              {/* Formatted Text */}
              <FormattedMessage text={msg.text} />

              {/* Tool Execution Badges */}
              {msg.tools && msg.tools.length > 0 && (
                <div className="mt-3 pt-2.5 border-t border-slate-800/80 flex flex-wrap items-center gap-1.5 text-[10px] text-slate-400">
                  <Cpu className="w-3 h-3 text-indigo-400" />
                  <span className="font-medium">Executed Tools:</span>
                  {msg.tools.map((tool, tIdx) => (
                    <span key={tIdx} className="px-2 py-0.5 bg-indigo-500/10 text-indigo-300 rounded font-mono border border-indigo-500/20">
                      {tool}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex items-center gap-3 p-3.5 bg-slate-900/80 rounded-xl border border-slate-800 text-xs text-indigo-300 animate-pulse w-fit shadow-md">
            <Sparkles className="w-4 h-4 animate-spin text-indigo-400" />
            <span>Analyzing SnapTrade holdings & generating response...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Prompt Chips */}
      <div className="p-3 border-t border-slate-800/60 bg-slate-950/80">
        <p className="text-[11px] text-slate-400 mb-2 font-medium">Suggested Questions:</p>
        <div className="flex flex-wrap gap-1.5">
          {PROMPT_CHIPS.map((chip, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(chip)}
              className="text-[11px] px-2.5 py-1 bg-slate-900 hover:bg-indigo-950/60 text-slate-300 hover:text-indigo-300 border border-slate-800 hover:border-indigo-500/30 rounded-lg transition text-left cursor-pointer flex items-center gap-1"
            >
              <span>{chip}</span>
              <ChevronRight className="w-3 h-3 text-slate-500" />
            </button>
          ))}
        </div>
      </div>

      {/* Input Box */}
      <div className="p-4 border-t border-slate-800 bg-slate-950">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex items-center gap-2"
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask ticker 'nvda' or your portfolio..."
            className="flex-1 bg-slate-900 text-slate-100 placeholder-slate-500 text-xs px-4 py-3 rounded-xl border border-slate-800 focus:outline-none focus:border-indigo-500 transition"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="p-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white rounded-xl transition shadow-lg shadow-indigo-600/30 cursor-pointer"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}
