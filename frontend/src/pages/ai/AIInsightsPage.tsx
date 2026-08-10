import React from 'react';
import { Sparkles, Bot, MessageSquare } from 'lucide-react';

export const AIInsightsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">AI Climate Insights & Advisories</h1>
        <p className="text-slate-400 text-sm mt-1">
          Explainable LLM Intelligence (Groq Llama-3.3-70B Provider)
        </p>
      </div>

      <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center min-h-[400px] text-center space-y-4">
        <div className="p-4 bg-amber-500/10 text-amber-400 rounded-full border border-amber-500/20">
          <Sparkles className="w-10 h-10" />
        </div>
        <div className="max-w-md space-y-2">
          <h3 className="text-lg font-semibold text-slate-200">Groq LLM Intelligence Container Wired</h3>
          <p className="text-sm text-slate-400">
            Groq Llama-3.3-70B API integration and prompt construction pipelines prepared. Executive summary generation scheduled for Sprint 3.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-950 px-3 py-1.5 rounded border border-slate-800 text-slate-400">
          <Bot className="w-3.5 h-3.5 text-amber-400" />
          <span>Endpoint: /api/v1/ai-report</span>
        </div>
      </div>
    </div>
  );
};
