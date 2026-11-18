import { useQuery } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import {
  ShieldAlert,
  AlertTriangle,
  BellRing,
  CloudRain,
  Waves,
  ArrowRight,
  MapPin,
  Bot,
  ExternalLink,
  Info,
} from 'lucide-react'

export default function DashboardPage() {
  const navigate = useNavigate()
  const { setSelectedRegionId } = useAppStore()

  const { data, isLoading, error } = useQuery({
    queryKey: ['dashboard-overview'],
    queryFn: () => apiService.getDashboard(),
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Loading coastal risk intelligence...</p>
        </div>
      </div>
    )
  }

  if (error || !data) {
    return (
      <div className="rounded-xl border border-rose-200 bg-rose-50 p-6 text-rose-800">
        <h2 className="text-base font-semibold">Unable to load dashboard data</h2>
        <p className="text-sm text-rose-600 mt-1">
          {error instanceof Error ? error.message : 'Backend connection error.'}
        </p>
      </div>
    )
  }

  const { kpis, today_situation, regions } = data

  const getRiskBadge = (level: string = 'Low', score: number = 0) => {
    switch (level) {
      case 'Critical':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">Critical ({score.toFixed(1)})</span>
      case 'High':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-900 border border-amber-300">High ({score.toFixed(1)})</span>
      case 'Moderate':
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-yellow-100 text-yellow-900 border border-yellow-200">Moderate ({score.toFixed(1)})</span>
      default:
        return <span className="px-2.5 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">Low ({score.toFixed(1)})</span>
    }
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* ── Page Header ────────────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Coastal Climate Risk Overview
          </h1>
          <p className="text-sm text-slate-500 mt-0.5">
            Real-time composite risk scoring, environmental sensors & AI-assisted coastal decision support
          </p>
        </div>
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/risk-map')}
            className="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm transition-colors"
          >
            <span>Explore GIS Map</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ── KPI Cards ──────────────────────────────────────────────── */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* KPI 1: Overall CCRI */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              {kpis.overall_risk_score.title}
            </span>
            <div className="p-2 rounded-lg bg-blue-50 text-blue-600">
              <ShieldAlert className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-900">
                {kpis.overall_risk_score.value}
              </span>
              <span className="text-xs font-medium text-slate-500">{kpis.overall_risk_score.unit}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{kpis.overall_risk_score.subtext}</p>
          </div>
        </div>

        {/* KPI 2: High Risk Zones */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              {kpis.high_risk_regions.title}
            </span>
            <div className="p-2 rounded-lg bg-amber-50 text-amber-600">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-900">
                {kpis.high_risk_regions.value}
              </span>
              <span className="text-xs font-medium text-slate-500">{kpis.high_risk_regions.unit}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{kpis.high_risk_regions.subtext}</p>
          </div>
        </div>

        {/* KPI 3: Active Alerts */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              {kpis.active_alerts.title}
            </span>
            <div className="p-2 rounded-lg bg-rose-50 text-rose-600">
              <BellRing className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-900">
                {kpis.active_alerts.value}
              </span>
              <span className="text-xs font-medium text-slate-500">{kpis.active_alerts.unit}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{kpis.active_alerts.subtext}</p>
          </div>
        </div>

        {/* KPI 4: Mean Rainfall */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              {kpis.average_rainfall.title}
            </span>
            <div className="p-2 rounded-lg bg-sky-50 text-sky-600">
              <CloudRain className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-900">
                {kpis.average_rainfall.value}
              </span>
              <span className="text-xs font-medium text-slate-500">{kpis.average_rainfall.unit}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{kpis.average_rainfall.subtext}</p>
          </div>
        </div>

        {/* KPI 5: Mean Tide */}
        <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
              {kpis.average_tide.title}
            </span>
            <div className="p-2 rounded-lg bg-teal-50 text-teal-600">
              <Waves className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-4">
            <div className="flex items-baseline gap-2">
              <span className="text-3xl font-extrabold text-slate-900">
                {kpis.average_tide.value}
              </span>
              <span className="text-xs font-medium text-slate-500">{kpis.average_tide.unit}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{kpis.average_tide.subtext}</p>
          </div>
        </div>
      </div>

      {/* ── Today's Situation & AI Executive Summary ────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Today's Situation */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="w-2.5 h-2.5 rounded-full bg-blue-600"></span>
                <h2 className="text-base font-bold text-slate-900">Today's Coastal Situation</h2>
              </div>
              <span className="text-xs font-medium text-slate-500">
                {today_situation.data_freshness}
              </span>
            </div>

            <div className="mt-4 p-4 rounded-lg bg-slate-50 border border-slate-200">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-semibold text-slate-900">
                  {today_situation.headline}
                </h3>
                {getRiskBadge(today_situation.overall_classification, today_situation.overall_score)}
              </div>
              <p className="text-sm text-slate-600 leading-relaxed">
                {today_situation.summary_text}
              </p>
            </div>

            <div className="mt-4">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-700 mb-2">
                Key Contributing Environmental Factors
              </h4>
              <ul className="space-y-1.5">
                {today_situation.main_contributors.map((factor, idx) => (
                  <li key={idx} className="flex items-start gap-2 text-sm text-slate-600">
                    <span className="text-blue-600 font-bold">•</span>
                    <span>{factor}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <div className="flex items-center gap-1.5 text-slate-500">
              <Info className="w-4 h-4 text-slate-400" />
              <span>{today_situation.methodology_disclosure}</span>
            </div>
          </div>
        </div>

        {/* AI Coastal Insights Card */}
        <div className="bg-gradient-to-br from-slate-900 to-blue-950 text-white rounded-xl p-6 shadow-md flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="p-1.5 rounded-md bg-blue-600/30 text-blue-400 border border-blue-500/30">
                  <Bot className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold tracking-wide">AI Decision Support</h3>
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-900/60 text-blue-300 border border-blue-700/50">
                Grounded Engine
              </span>
            </div>

            <div className="mt-4 space-y-3">
              <p className="text-xs text-slate-300 leading-relaxed">
                Automated multi-factor risk synthesis grounded in deterministic CCRI scores.
                Explains vulnerabilities and recommends proactive mitigation for disaster authorities.
              </p>

              <div className="p-3 rounded-lg bg-white/5 border border-white/10 space-y-2">
                <span className="text-[11px] font-semibold uppercase text-blue-300 tracking-wider">
                  Operational Recommendation:
                </span>
                <p className="text-xs text-slate-200">
                  Prioritize estuarine drainage clearing in Sundarbans and Kochi Backwaters ahead of high spring tide cycles.
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 pt-4 border-t border-white/10 flex items-center justify-between">
            <button
              onClick={() => navigate('/ai-insights')}
              className="w-full inline-flex items-center justify-center gap-2 px-4 py-2 text-xs font-semibold rounded-lg bg-blue-600 hover:bg-blue-500 text-white transition-colors"
            >
              <span>Open AI Insights Module</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* ── Regional Risk Comparison Matrix ────────────────────────── */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
          <div>
            <h2 className="text-base font-bold text-slate-900">Regional Coastal Risk Matrix</h2>
            <p className="text-xs text-slate-500">
              Evaluated using Phase 5 Composite Climate Risk Index (Weights: Rain 35%, Tide 30%, Elev 20%, Flood 15%)
            </p>
          </div>
          <button
            onClick={() => navigate('/analytics')}
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            <span>Detailed Analytics</span>
            <ExternalLink className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm text-slate-600">
            <thead className="bg-slate-50 text-xs font-semibold uppercase tracking-wider text-slate-500 border-b border-slate-200">
              <tr>
                <th className="px-6 py-3.5">Coastal Zone</th>
                <th className="px-6 py-3.5">State / District</th>
                <th className="px-6 py-3.5">Rainfall (24h)</th>
                <th className="px-6 py-3.5">Tide Height</th>
                <th className="px-6 py-3.5">Elevation</th>
                <th className="px-6 py-3.5">Flood Profile</th>
                <th className="px-6 py-3.5">CCRI Score</th>
                <th className="px-6 py-3.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {regions.map((reg) => {
                const risk = reg.latest_risk
                const score = risk?.final_score ?? 0.0
                const level = risk?.risk_level ?? 'Low'

                return (
                  <tr
                    key={reg.id}
                    className="hover:bg-slate-50/80 transition-colors cursor-pointer"
                    onClick={() => {
                      setSelectedRegionId(reg.id)
                      navigate('/risk-map')
                    }}
                  >
                    <td className="px-6 py-4 font-semibold text-slate-900 flex items-center gap-2">
                      <MapPin className="w-4 h-4 text-blue-600 flex-shrink-0" />
                      <span>{reg.name}</span>
                    </td>
                    <td className="px-6 py-4 text-slate-600">
                      {reg.district}, {reg.state}
                    </td>
                    <td className="px-6 py-4 text-slate-900">
                      {reg.latest_rainfall_mm?.toFixed(1) ?? '—'} mm
                    </td>
                    <td className="px-6 py-4 text-slate-900">
                      {reg.latest_tide_m?.toFixed(2) ?? '—'} m
                    </td>
                    <td className="px-6 py-4 text-slate-900">
                      {reg.elevation_m} m
                    </td>
                    <td className="px-6 py-4 capitalize text-slate-700">
                      {reg.flood_severity}
                    </td>
                    <td className="px-6 py-4">
                      {getRiskBadge(level, score)}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedRegionId(reg.id)
                            navigate('/risk-map')
                          }}
                          className="px-2.5 py-1 text-xs font-semibold text-blue-600 hover:bg-blue-50 rounded border border-blue-200 transition-colors"
                        >
                          Map
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation()
                            setSelectedRegionId(reg.id)
                            navigate('/analytics')
                          }}
                          className="px-2.5 py-1 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded border border-slate-200 transition-colors"
                        >
                          Stats
                        </button>
                      </div>
                    </td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
