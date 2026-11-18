import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Map,
  BarChart2,
  Bot,
  FileText,
  Info,
  Waves,
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard, end: true },
  { to: '/risk-map', label: 'Risk Map', icon: Map, end: false },
  { to: '/analytics', label: 'Analytics', icon: BarChart2, end: false },
  { to: '/ai-insights', label: 'AI Insights', icon: Bot, end: false },
  { to: '/reports', label: 'Reports', icon: FileText, end: false },
  { to: '/about', label: 'About Project', icon: Info, end: false },
] as const

export default function Sidebar() {
  return (
    <aside className="w-64 flex-shrink-0 bg-slate-900 border-r border-slate-800 flex flex-col text-slate-100">
      {/* ── Project identity ─────────────────────────────────────────── */}
      <div className="px-5 py-5 border-b border-slate-800 flex items-center gap-3">
        <div className="w-9 h-9 rounded-lg bg-blue-600 flex items-center justify-center flex-shrink-0 shadow-md">
          <Waves className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="text-sm font-bold text-white tracking-wide">
            Coastal Climate Risk
          </h1>
          <p className="text-xs text-slate-400">Intelligence Platform</p>
        </div>
      </div>

      {/* ── Navigation links ─────────────────────────────────────────── */}
      <nav className="flex-1 px-3 py-4 space-y-1" aria-label="Primary navigation">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            className={({ isActive }) =>
              [
                'flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-colors duration-150',
                isActive
                  ? 'bg-blue-600 text-white font-semibold shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white',
              ].join(' ')
            }
          >
            <Icon className="w-4 h-4 flex-shrink-0" aria-hidden="true" />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* ── Footer ───────────────────────────────────────────────────── */}
      <div className="px-5 py-4 border-t border-slate-800 text-xs text-slate-400 space-y-1">
        <div className="flex items-center justify-between">
          <span>Prototype Edition</span>
          <span className="px-1.5 py-0.5 rounded bg-blue-900/60 text-blue-300 font-mono text-[10px]">
            v1.0.0
          </span>
        </div>
        <p className="text-[11px] text-slate-500">
          CCRI Phase 5 & 6 Integrated
        </p>
      </div>
    </aside>
  )
}
