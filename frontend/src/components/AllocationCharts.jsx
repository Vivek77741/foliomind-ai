import React, { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { Layers, PieChart as PieIcon } from 'lucide-react';

const COLORS = ['#6366f1', '#10b981', '#a855f7', '#3b82f6', '#f59e0b', '#ec4899', '#64748b'];

export default function AllocationCharts({ allocation }) {
  const [activeTab, setActiveTab] = useState('sector');

  if (!allocation) return null;

  const data = activeTab === 'sector' ? allocation.by_sector : allocation.by_asset_class;

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const item = payload[0].payload;
      return (
        <div className="glass-card p-3 rounded-xl border border-slate-700/50 shadow-xl text-xs">
          <p className="font-semibold text-slate-200 mb-1">{item.name}</p>
          <p className="text-indigo-400 font-bold">${item.value?.toLocaleString()}</p>
          <p className="text-slate-400">{item.percentage}% of portfolio</p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-card p-6 rounded-2xl mb-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
        <div>
          <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2">
            <PieIcon className="w-5 h-5 text-indigo-400" />
            Asset & Sector Allocation
          </h3>
          <p className="text-xs text-slate-400">Visual breakdown of your holdings retrieved via SnapTrade API</p>
        </div>

        {/* Tab Toggle */}
        <div className="flex p-1 bg-slate-900/80 rounded-xl border border-slate-800 self-start sm:self-auto">
          <button
            onClick={() => setActiveTab('sector')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              activeTab === 'sector'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            By Sector
          </button>
          <button
            onClick={() => setActiveTab('asset')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition cursor-pointer ${
              activeTab === 'asset'
                ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            By Asset Class
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        {/* Donut Chart */}
        <div className="lg:col-span-6 h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                innerRadius={65}
                outerRadius={95}
                paddingAngle={4}
                dataKey="value"
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} stroke="rgba(15, 23, 42, 0.8)" strokeWidth={2} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Legend List */}
        <div className="lg:col-span-6 space-y-2.5 max-h-64 overflow-y-auto pr-2">
          {data.map((item, index) => (
            <div key={item.name} className="flex items-center justify-between p-2.5 rounded-xl bg-slate-900/40 border border-slate-800/60 text-xs">
              <div className="flex items-center gap-2.5">
                <span className="w-3 h-3 rounded-full flex-shrink-0" style={{ backgroundColor: COLORS[index % COLORS.length] }}></span>
                <span className="font-medium text-slate-200">{item.name}</span>
              </div>
              <div className="text-right">
                <span className="font-bold text-slate-100">${item.value?.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                <span className="text-slate-400 ml-2 font-medium">({item.percentage}%)</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
