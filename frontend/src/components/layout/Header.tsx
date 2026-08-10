import React from 'react';
import { ShieldCheck } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header className="h-16 bg-slate-900/80 backdrop-blur-sm border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-10">
      <div className="flex items-center space-x-3">
        <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20 flex items-center space-x-1.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <span>System Foundation Active</span>
        </span>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 text-xs text-slate-400">
          <ShieldCheck className="w-4 h-4 text-sky-400" />
          <span>PostGIS + FastAPI Stack</span>
        </div>
      </div>
    </header>
  );
};
