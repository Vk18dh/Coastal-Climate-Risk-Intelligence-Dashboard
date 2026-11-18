import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import type { ClimateRiskReport } from '@/types'
import {
  FileText,
  Printer,
  MapPin,
  Sparkles,
} from 'lucide-react'

export default function ReportsPage() {
  const { selectedRegionId, setSelectedRegionId } = useAppStore()
  const [activeReport, setActiveReport] = useState<ClimateRiskReport | null>(null)

  // Fetch Regions
  const { data: regions } = useQuery({
    queryKey: ['regions'],
    queryFn: () => apiService.getRegions(),
  })

  // Fetch Reports list
  const { data: reportsList, refetch: refetchReports } = useQuery({
    queryKey: ['reports-list'],
    queryFn: () => apiService.getReports(),
  })

  // Generate Report Mutation
  const generateMutation = useMutation({
    mutationFn: () => apiService.generateReport(selectedRegionId, true, true),
    onSuccess: (newReport) => {
      setActiveReport(newReport)
      refetchReports()
    },
  })

  const currentRegion = regions?.find((r) => r.id === selectedRegionId)

  const handlePrint = () => {
    window.print()
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* ── Page Header ────────────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4 print:hidden">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <FileText className="w-6 h-6 text-blue-600" />
            <span>Regional Climate Risk Assessment Reports</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Automated compilation of environmental metrics, deterministic CCRI scores, statistical trends & AI advisory
          </p>
        </div>

        {/* Generate Controls */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-xs">
            <MapPin className="w-4 h-4 text-blue-600" />
            <span className="text-xs font-semibold text-slate-500">Region:</span>
            <select
              value={selectedRegionId}
              onChange={(e) => setSelectedRegionId(Number(e.target.value))}
              className="text-xs font-semibold text-slate-900 bg-transparent focus:outline-none"
            >
              {regions?.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.name}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => generateMutation.mutate()}
            disabled={generateMutation.isPending}
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-xs transition-colors disabled:opacity-50"
          >
            {generateMutation.isPending ? (
              <>
                <div className="w-3.5 h-3.5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Compiling Report...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                <span>Generate Assessment Report</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* ── Reports Split: List on Left (if exists) / Full Report on Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Past Reports History (4 cols) */}
        <div className="lg:col-span-4 bg-white rounded-2xl border border-slate-200 p-5 shadow-xs space-y-4 print:hidden">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h2 className="text-sm font-bold text-slate-900">Generated Reports Archive</h2>
            <span className="text-xs font-mono text-slate-500">{reportsList?.length || 0} reports</span>
          </div>

          <div className="space-y-2 max-h-[560px] overflow-y-auto">
            {reportsList && reportsList.length > 0 ? (
              reportsList.map((rep) => (
                <div
                  key={rep.report_id}
                  onClick={() => setActiveReport(rep)}
                  className={`p-3.5 rounded-xl border text-xs cursor-pointer transition-all ${
                    activeReport?.report_id === rep.report_id
                      ? 'border-blue-600 bg-blue-50/60 shadow-xs'
                      : 'border-slate-200 hover:bg-slate-50'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-slate-900">{rep.region_name}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-200 text-slate-800">
                      {rep.current_ccri.risk_level}
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-slate-500 mt-2 text-[11px]">
                    <span className="font-mono text-blue-700 font-semibold">{rep.report_id}</span>
                    <span>{new Date(rep.generated_at).toLocaleDateString()}</span>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center py-10 text-slate-400 text-xs">
                <FileText className="w-8 h-8 mx-auto mb-2 opacity-50" />
                <p>No reports generated yet.</p>
                <p className="mt-1">Click &ldquo;Generate Assessment Report&rdquo; above.</p>
              </div>
            )}
          </div>
        </div>

        {/* Full Report Document View (8 cols) */}
        <div className="lg:col-span-8">
          {activeReport ? (
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-8 space-y-6 print:border-none print:shadow-none print:p-0">
              {/* Report Header Bar */}
              <div className="flex items-center justify-between border-b-2 border-slate-900 pb-5">
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-widest text-blue-600">
                    Official Environmental Intelligence Document
                  </span>
                  <h2 className="text-2xl font-black text-slate-900 mt-1">
                    {activeReport.title}
                  </h2>
                  <p className="text-xs text-slate-500 mt-0.5">
                    District: {activeReport.district} · State: {activeReport.state} · Document ID:{' '}
                    <span className="font-mono font-semibold text-slate-700">{activeReport.report_id}</span>
                  </p>
                </div>

                <div className="flex items-center gap-2 print:hidden">
                  <button
                    onClick={handlePrint}
                    className="p-2 rounded-lg border border-slate-300 hover:bg-slate-50 text-slate-700 text-xs font-semibold flex items-center gap-1.5 shadow-xs transition-colors"
                  >
                    <Printer className="w-4 h-4 text-slate-500" />
                    <span>Print / PDF</span>
                  </button>
                </div>
              </div>

              {/* Assessment Meta Strip */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs">
                <div>
                  <span className="text-slate-400 font-medium">Evaluation Date</span>
                  <p className="font-bold text-slate-900 mt-0.5">
                    {new Date(activeReport.generated_at).toLocaleDateString()}
                  </p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">CCRI Score</span>
                  <p className="font-bold text-blue-600 mt-0.5 text-sm">
                    {activeReport.current_ccri.final_score?.toFixed(1)}/100
                  </p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Risk Level</span>
                  <p className="font-bold text-slate-900 mt-0.5 uppercase">
                    {activeReport.current_ccri.risk_level}
                  </p>
                </div>
                <div>
                  <span className="text-slate-400 font-medium">Data Completeness</span>
                  <p className="font-bold text-slate-900 mt-0.5">
                    {(activeReport.current_ccri.data_completeness * 100).toFixed(0)}%
                  </p>
                </div>
              </div>

              {/* Executive Summary */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  1. Executive Summary
                </h3>
                <p className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200">
                  {activeReport.executive_summary}
                </p>
              </div>

              {/* Observed Environmental Metrics */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  2. Environmental Parameters & Coastal Geography
                </h3>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                  <div className="p-3 rounded-lg border border-slate-200">
                    <span className="text-slate-500">24h Rainfall:</span>
                    <p className="font-bold text-slate-900 mt-0.5">
                      {activeReport.environmental_overview.latest_rainfall_mm} mm
                    </p>
                  </div>
                  <div className="p-3 rounded-lg border border-slate-200">
                    <span className="text-slate-500">Tidal Level:</span>
                    <p className="font-bold text-slate-900 mt-0.5">
                      {activeReport.environmental_overview.latest_tide_meters} m
                    </p>
                  </div>
                  <div className="p-3 rounded-lg border border-slate-200">
                    <span className="text-slate-500">Topography Elevation:</span>
                    <p className="font-bold text-slate-900 mt-0.5">
                      {activeReport.environmental_overview.mean_elevation_meters} m
                    </p>
                  </div>
                  <div className="p-3 rounded-lg border border-slate-200">
                    <span className="text-slate-500">Historical Flood Risk:</span>
                    <p className="font-bold text-slate-900 mt-0.5 capitalize">
                      {activeReport.environmental_overview.historical_flood_severity}
                    </p>
                  </div>
                </div>
              </div>

              {/* CCRI Score Breakdown Table */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  3. Deterministic CCRI Component Contributions
                </h3>
                <div className="overflow-x-auto border border-slate-200 rounded-xl">
                  <table className="w-full text-left text-xs text-slate-700">
                    <thead className="bg-slate-50 font-semibold text-slate-500 border-b border-slate-200">
                      <tr>
                        <th className="px-4 py-2.5">Component</th>
                        <th className="px-4 py-2.5">Normalized Score</th>
                        <th className="px-4 py-2.5">Original Weight</th>
                        <th className="px-4 py-2.5">Effective Weight</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                      {Object.entries(activeReport.current_ccri.component_scores).map(([comp, score]) => {
                        const origWeight = activeReport.current_ccri.original_weights[comp] ?? 0
                        const effWeight = activeReport.current_ccri.effective_weights[comp] ?? 0
                        return (
                          <tr key={comp}>
                            <td className="px-4 py-2 font-medium text-slate-900 capitalize">
                              {comp.replace('_score', '')}
                            </td>
                            <td className="px-4 py-2 font-mono">{(score * 100).toFixed(1)}/100</td>
                            <td className="px-4 py-2 font-mono">{(origWeight * 100).toFixed(0)}%</td>
                            <td className="px-4 py-2 font-mono font-bold text-blue-700">
                              {(effWeight * 100).toFixed(0)}%
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Recommended Precautionary Actions */}
              <div className="space-y-2">
                <h3 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  4. Operational Precautionary Recommendations
                </h3>
                <ul className="space-y-1.5 text-xs text-slate-700 bg-slate-50 p-4 rounded-xl border border-slate-200">
                  {activeReport.recommended_actions.map((act, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="font-bold text-emerald-700">{idx + 1}.</span>
                      <span>{act}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Provenance & Disclaimer Footer */}
              <div className="pt-4 border-t border-slate-200 space-y-2 text-[11px] text-slate-500">
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span>Methodology: {activeReport.current_ccri.methodology_version}</span>
                  <span>Weather: Open-Meteo Baseline · Tide: Hydrodynamic Mock</span>
                </div>
                <p className="italic text-slate-400">{activeReport.disclaimer}</p>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-500">
              <FileText className="w-10 h-10 text-slate-300 mx-auto mb-3" />
              <h3 className="text-base font-bold text-slate-800">No Assessment Report Selected</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                Select a previous report from the archive on the left, or generate a fresh climate assessment for{' '}
                <strong>{currentRegion?.name}</strong>.
              </p>
              <button
                onClick={() => generateMutation.mutate()}
                className="mt-4 px-4 py-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs transition-colors shadow-xs"
              >
                Generate Report for {currentRegion?.name.split(' ')[0]}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
