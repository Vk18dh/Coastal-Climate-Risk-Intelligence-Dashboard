import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import {
  PieChart as PieIcon,
  GitCommit,
  Info,
  Calendar,
} from 'lucide-react'

const RISK_COLORS = {
  Low: '#10b981',
  Moderate: '#eab308',
  High: '#f97316',
  Critical: '#ef4444',
}

export default function AnalyticsPage() {
  const { selectedRegionId, setSelectedRegionId, timeRangeDays, setTimeRangeDays } = useAppStore()
  const [selectedMetric, setSelectedMetric] = useState<'rainfall' | 'tide' | 'risk'>('rainfall')

  // Fetch Regions list
  const { data: regions } = useQuery({
    queryKey: ['regions'],
    queryFn: () => apiService.getRegions(),
  })

  // Fetch Timeseries for selected region & metric
  const { data: timeseriesData } = useQuery({
    queryKey: ['analytics-timeseries', selectedRegionId, selectedMetric, timeRangeDays],
    queryFn: () => apiService.getTimeseries(selectedRegionId, selectedMetric, timeRangeDays),
  })

  // Fetch Risk Distribution
  const { data: distributionData } = useQuery({
    queryKey: ['analytics-distribution', selectedRegionId, timeRangeDays],
    queryFn: () => apiService.getRiskDistribution(selectedRegionId, timeRangeDays),
  })

  // Fetch Correlation between rainfall and risk
  const { data: correlationData } = useQuery({
    queryKey: ['analytics-correlation', selectedRegionId, 'rainfall', 'risk', timeRangeDays],
    queryFn: () => apiService.getCorrelation(selectedRegionId, 'rainfall', 'risk', timeRangeDays),
  })

  // Fetch Regional Comparison
  const { data: comparisonData } = useQuery({
    queryKey: ['analytics-comparison', selectedMetric, timeRangeDays],
    queryFn: () => apiService.getComparison(selectedMetric, timeRangeDays),
  })

  const currentRegion = regions?.find((r) => r.id === selectedRegionId)

  // Format timeseries for Recharts
  const chartPoints = timeseriesData?.observations.map((obs) => ({
    date: obs.timestamp.split('T')[0].slice(5),
    value: obs.value,
  })) || []

  // Format distribution for PieChart
  const pieData = distributionData?.distribution
    ? Object.entries(distributionData.distribution).map(([name, value]) => ({
        name,
        value,
      }))
    : []

  // Format comparison data for BarChart
  const barData = comparisonData?.regions.map((comp) => {
    const reg = regions?.find((r) => r.id === comp.region_id)
    return {
      name: reg ? reg.name.split(' ')[0] : `Region ${comp.region_id}`,
      mean: comp.statistics.mean ?? 0,
      max: comp.statistics.max ?? 0,
    }
  }) || []

  const stats = timeseriesData?.statistics

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* ── Page Header ────────────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
            Statistical Climate Analytics
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Temporal alignment, sample standard deviation, descriptive trends & Pearson correlation (Phase 6 Spec)
          </p>
        </div>

        {/* Global Filter Bar */}
        <div className="flex flex-wrap items-center gap-3">
          {/* Region Dropdown */}
          <div className="flex items-center gap-2 bg-white border border-slate-200 px-3 py-1.5 rounded-lg shadow-xs">
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

          {/* Time Window Buttons */}
          <div className="flex items-center gap-1 bg-white border border-slate-200 p-1 rounded-lg shadow-xs">
            <Calendar className="w-3.5 h-3.5 text-slate-400 ml-1.5" />
            {[7, 14, 30].map((days) => (
              <button
                key={days}
                onClick={() => setTimeRangeDays(days)}
                className={`px-2.5 py-1 text-xs font-semibold rounded transition-colors ${
                  timeRangeDays === days
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                {days}d
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* ── Metric Selector Tabs ───────────────────────────────────── */}
      <div className="flex items-center gap-2 border-b border-slate-200 pb-2">
        {(['rainfall', 'tide', 'risk'] as const).map((metric) => (
          <button
            key={metric}
            onClick={() => setSelectedMetric(metric)}
            className={`px-4 py-2 rounded-lg text-xs font-bold uppercase tracking-wider transition-colors ${
              selectedMetric === metric
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-600 hover:bg-slate-100'
            }`}
          >
            {metric === 'rainfall'
              ? 'Rainfall (mm)'
              : metric === 'tide'
              ? 'Tide Level (m)'
              : 'CCRI Score (0-100)'}
          </button>
        ))}
      </div>

      {/* ── Descriptive Statistics KPI Strip ───────────────────────── */}
      {stats && (
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Valid Obs (n)</span>
            <p className="text-xl font-bold text-slate-900 mt-1">{stats.count}</p>
            <p className="text-[10px] text-slate-500">Paired daily points</p>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Mean</span>
            <p className="text-xl font-bold text-slate-900 mt-1">
              {stats.mean !== null ? stats.mean : '—'}
            </p>
            <p className="text-[10px] text-slate-500">Arithmetic average</p>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Median</span>
            <p className="text-xl font-bold text-slate-900 mt-1">
              {stats.median !== null ? stats.median : '—'}
            </p>
            <p className="text-[10px] text-slate-500">50th percentile</p>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Sample Stddev</span>
            <p className="text-xl font-bold text-blue-600 mt-1">
              {stats.sample_stddev !== null ? stats.sample_stddev : '—'}
            </p>
            <p className="text-[10px] text-slate-500">n-1 degrees of freedom</p>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Min / Max</span>
            <p className="text-xl font-bold text-slate-900 mt-1">
              {stats.min} / {stats.max}
            </p>
            <p className="text-[10px] text-slate-500">Observed bounds</p>
          </div>

          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-xs">
            <span className="text-[11px] font-semibold uppercase text-slate-400">Historical Trend</span>
            <p className="text-xl font-bold text-slate-900 mt-1">
              {stats.trend?.percentage_change != null
                ? `${stats.trend.percentage_change > 0 ? '+' : ''}${stats.trend.percentage_change}%`
                : '—'}
            </p>
            <p className="text-[10px] text-slate-500">
              {stats.trend?.first_value} &rarr; {stats.trend?.last_value}
            </p>
          </div>
        </div>
      )}

      {/* ── Main Timeseries Chart ──────────────────────────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="text-base font-bold text-slate-900">
              {currentRegion?.name}: {selectedMetric.toUpperCase()} Timeseries
            </h2>
            <p className="text-xs text-slate-500">
              Daily observations aggregated over {timeRangeDays} days · Source:{' '}
              {timeseriesData?.provenance[selectedMetric] || 'System Data'}
            </p>
          </div>
          <span className="text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-medium">
            Strictly Historical (No forecasting)
          </span>
        </div>

        <div className="h-72 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartPoints} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} />
              <YAxis stroke="#94a3b8" fontSize={11} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                itemStyle={{ color: '#38bdf8', fontSize: '12px' }}
                labelStyle={{ color: '#f8fafc', fontWeight: 'bold', fontSize: '11px' }}
              />
              <Line
                type="monotone"
                dataKey="value"
                stroke={selectedMetric === 'rainfall' ? '#0284c7' : selectedMetric === 'tide' ? '#0d9488' : '#e11d48'}
                strokeWidth={2.5}
                dot={{ r: 3, fill: '#ffffff', strokeWidth: 2 }}
                activeDot={{ r: 6 }}
                name={selectedMetric}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* ── Grid: Distribution & Correlation ───────────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Risk Distribution (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <PieIcon className="w-4 h-4 text-blue-600" />
                <span>Risk Level Distribution</span>
              </h3>
              <span className="text-xs text-slate-500 font-mono">n = {distributionData?.count || 0}</span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Percentage breakdown across risk tiers in {currentRegion?.name}
            </p>

            <div className="h-56 w-full mt-4 flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry) => (
                      <Cell
                        key={`cell-${entry.name}`}
                        fill={RISK_COLORS[entry.name as keyof typeof RISK_COLORS] || '#94a3b8'}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                    itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
                  />
                  <Legend verticalAlign="bottom" height={36} wrapperStyle={{ fontSize: '11px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>Evaluated by CCRI Engine</span>
            <span>Provenance: PostgreSQL/Demo</span>
          </div>
        </div>

        {/* Pearson Correlation & Association (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl border border-slate-200 p-6 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                <GitCommit className="w-4 h-4 text-blue-600" />
                <span>Correlation Analysis: Rainfall vs CCRI Risk</span>
              </h3>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold">
                r = {correlationData?.correlation !== null ? correlationData?.correlation : '—'}
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-0.5">
              Pearson correlation calculated on strictly paired daily observations (n = {correlationData?.paired_observation_count || 0})
            </p>

            {/* Explanation box */}
            <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
              <div className="flex items-center gap-2 text-xs font-bold text-slate-800">
                <Info className="w-4 h-4 text-blue-600" />
                <span>Interpretation: Statistical Association, Not Causation</span>
              </div>
              <p className="text-xs text-slate-600 leading-relaxed">
                The computed correlation coefficient of{' '}
                <strong className="text-slate-900">{correlationData?.correlation}</strong> indicates a{' '}
                {(correlationData?.correlation || 0) > 0.7
                  ? 'strong positive statistical association'
                  : 'moderate correlation'}{' '}
                between daily precipitation levels and overall Composite Climate Risk Index (CCRI) fluctuations.
                Per Phase 6 requirements, correlation implies statistical co-movement and does not assert direct physical causation.
              </p>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-3 text-xs">
              <div className="p-3 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 font-medium">Variable X:</span>
                <p className="font-bold text-slate-800 capitalize mt-0.5">Rainfall (mm)</p>
                <p className="text-[10px] text-slate-500">Provenance: Open-Meteo</p>
              </div>
              <div className="p-3 rounded-lg border border-slate-200 bg-white">
                <span className="text-slate-400 font-medium">Variable Y:</span>
                <p className="font-bold text-slate-800 capitalize mt-0.5">CCRI Risk Score (0-100)</p>
                <p className="text-[10px] text-slate-500">Provenance: Climate Risk Engine</p>
              </div>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 text-xs text-slate-500">
            <span>Temporal Alignment: Daily Mean Grouping with Complete Paired Observations</span>
          </div>
        </div>
      </div>

      {/* ── Multi-Region Comparison Bar Chart ──────────────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-base font-bold text-slate-900">
              Cross-Regional Comparison ({selectedMetric.toUpperCase()})
            </h3>
            <p className="text-xs text-slate-500">
              Mean and Peak (Max) values observed across all coastal zones over the last {timeRangeDays} days
            </p>
          </div>
        </div>

        <div className="h-64 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="name" stroke="#94a3b8" fontSize={11} />
              <YAxis stroke="#94a3b8" fontSize={11} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                itemStyle={{ color: '#f8fafc', fontSize: '12px' }}
              />
              <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: '11px' }} />
              <Bar dataKey="mean" fill="#3b82f6" name="Mean Value" radius={[4, 4, 0, 0]} />
              <Bar dataKey="max" fill="#93c5fd" name="Peak (Max)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
