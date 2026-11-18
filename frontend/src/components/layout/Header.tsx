import { useQuery } from '@tanstack/react-query'
import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import { ShieldCheck, MapPin, Database } from 'lucide-react'

export default function Header() {
  const { selectedRegionId, setSelectedRegionId } = useAppStore()

  const { data: regions } = useQuery({
    queryKey: ['regions'],
    queryFn: () => apiService.getRegions(),
  })

  return (
    <header className="h-16 bg-white border-b border-gray-200 px-6 flex items-center justify-between flex-shrink-0">
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <MapPin className="w-4 h-4 text-blue-600" />
          <span className="text-xs font-semibold uppercase tracking-wider text-gray-500">
            Selected Coastal Zone:
          </span>
          <select
            value={selectedRegionId}
            onChange={(e) => setSelectedRegionId(Number(e.target.value))}
            className="text-sm font-medium text-gray-900 bg-gray-50 border border-gray-300 rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {regions?.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name} ({r.district}, {r.state || 'India'})
              </option>
            )) || <option value={1}>Chennai Coastal Zone</option>}
          </select>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Baseline Data Status */}
        <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-full text-xs text-slate-700">
          <Database className="w-3.5 h-3.5 text-blue-600" />
          <span>Demo Data Baseline</span>
        </div>

        {/* Engine Status */}
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-full text-xs text-emerald-800 font-medium">
          <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
          <span>CCRI Engine v1.0.0</span>
        </div>

        {/* System telemetry indicator */}
        <div className="flex items-center gap-1.5 text-xs text-gray-500">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>System Active</span>
        </div>
      </div>
    </header>
  )
}
