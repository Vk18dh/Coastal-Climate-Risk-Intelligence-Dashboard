import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  MapPin, 
  BarChart3, 
  Sparkles, 
  FileText, 
  Info,
  Waves
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/risk-map', label: 'Risk Map', icon: MapPin },
  { path: '/analytics', label: 'Analytics', icon: BarChart3 },
  { path: '/ai-insights', label: 'AI Insights', icon: Sparkles },
  { path: '/reports', label: 'Reports', icon: FileText },
  { path: '/about', label: 'About', icon: Info },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen sticky top-0">
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="p-2 bg-sky-500/10 text-sky-400 rounded-lg border border-sky-500/20">
          <Waves className="w-6 h-6" />
        </div>
        <div>
          <h1 className="font-bold text-sm text-slate-100 leading-tight">Coastal Risk</h1>
          <p className="text-xs text-slate-400">Intelligence Platform</p>
        </div>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-sky-600 text-white shadow-lg shadow-sky-600/20'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      <div className="p-4 border-t border-slate-800">
        <div className="px-3 py-2 bg-slate-950/60 rounded-md border border-slate-800 text-xs text-slate-400">
          <p className="font-medium text-slate-300">Environment</p>
          <p>Development Foundation</p>
        </div>
      </div>
    </aside>
  );
};
