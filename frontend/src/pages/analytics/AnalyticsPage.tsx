import React from 'react';
import { BarChart3, TrendingUp, LineChart } from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Statistical Climate Analytics</h1>
        <p className="text-slate-400 text-sm mt-1">
          Rainfall Trends, Tide Levels, Time-Series & Historical Correlations
        </p>
      </div>

      <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center min-h-[400px] text-center space-y-4">
        <div className="p-4 bg-purple-500/10 text-purple-400 rounded-full border border-purple-500/20">
          <BarChart3 className="w-10 h-10" />
        </div>
        <div className="max-w-md space-y-2">
          <h3 className="text-lg font-semibold text-slate-200">Statistical Engine Foundation Wired</h3>
          <p className="text-sm text-slate-400">
            Recharts visualization container and API client wired. Time series, rainfall-tide correlations, and statistical distributions scheduled for Sprint 3.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-950 px-3 py-1.5 rounded border border-slate-800 text-slate-400">
          <LineChart className="w-3.5 h-3.5 text-purple-400" />
          <span>Endpoint: /api/v1/analytics</span>
        </div>
      </div>
    </div>
  );
};
