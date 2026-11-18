import {
  ShieldAlert,
  HelpCircle,
  Cpu,
  Database,
  Waves,
  CloudRain,
  Mountain,
  AlertTriangle,
} from 'lucide-react'

export default function AboutPage() {
  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-14 text-slate-800">
      {/* ── Page Header ────────────────────────────────────────────── */}
      <div className="border-b border-slate-200 pb-5">
        <span className="text-xs font-bold uppercase tracking-widest text-blue-600">
          Architecture & Methodology Documentation
        </span>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight mt-1">
          Coastal Climate Risk Intelligence Platform
        </h1>
        <p className="text-sm text-slate-600 mt-1 max-w-3xl leading-relaxed">
          An integrated AI-powered, GIS-based coastal decision-support system designed to assess,
          visualize, explain, and mitigate climate-related compound hazards across vulnerable coastal zones.
        </p>
      </div>

      {/* ── 4 Core Questions Answered ───────────────────────────────── */}
      <div className="space-y-4">
        <h2 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <HelpCircle className="w-5 h-5 text-blue-600" />
          <span>The Four Core Questions Answered</span>
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                1
              </span>
              <h3 className="font-bold text-slate-900 text-sm">What is happening?</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Real-time monitoring of atmospheric and oceanographic observations: precipitation levels,
              astronomical tide cycles, and storm surge anomalies across peninsular coastal tracts.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                2
              </span>
              <h3 className="font-bold text-slate-900 text-sm">Where is the risk?</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Interactive GIS visualization projecting composite risk scores onto geographic administrative
              boundaries, identifying hyper-local low-elevation vulnerable zones and estuaries.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                3
              </span>
              <h3 className="font-bold text-slate-900 text-sm">Why is the region at risk?</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Transparent, deterministic decomposition of the Composite Climate Risk Index (CCRI) into normalized
              rainfall, tidal height, topographic elevation, and historical flood severity components.
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-2">
            <div className="flex items-center gap-2">
              <span className="w-6 h-6 rounded-full bg-blue-100 text-blue-800 font-bold text-xs flex items-center justify-center">
                4
              </span>
              <h3 className="font-bold text-slate-900 text-sm">What actions should be considered?</h3>
            </div>
            <p className="text-xs text-slate-600 leading-relaxed">
              Actionable operational advisories tailored to municipal authorities, emergency teams, and
              planners—ranging from sluice gate control to mobile pump pre-positioning.
            </p>
          </div>
        </div>
      </div>

      {/* ── Climate Risk Engine (Phase 5 Methodology) ──────────────── */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-5">
        <div className="flex items-center justify-between border-b border-slate-100 pb-3">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-blue-600" />
            <h2 className="text-base font-bold text-slate-900">
              Composite Climate Risk Index (CCRI) Methodology
            </h2>
          </div>
          <span className="text-xs font-mono px-2 py-0.5 rounded bg-blue-50 text-blue-700 font-bold">
            Methodology: demo-v1.0
          </span>
        </div>

        <p className="text-xs text-slate-600 leading-relaxed">
          The CCRI formula combines multi-hazard physical parameters into a deterministic, reproducible scalar score
          between 0.0 and 100.0. The engine strictly runs on the backend to maintain single-source-of-truth mathematical integrity.
        </p>

        {/* Weights Table */}
        <div className="overflow-x-auto border border-slate-200 rounded-xl">
          <table className="w-full text-left text-xs text-slate-700">
            <thead className="bg-slate-50 font-semibold text-slate-500 border-b border-slate-200">
              <tr>
                <th className="px-4 py-2.5">Component</th>
                <th className="px-4 py-2.5">Original Weight</th>
                <th className="px-4 py-2.5">Normalization Bounds</th>
                <th className="px-4 py-2.5">Behavioral Logic</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr>
                <td className="px-4 py-2.5 font-semibold text-slate-900 flex items-center gap-1.5">
                  <CloudRain className="w-3.5 h-3.5 text-sky-600" />
                  <span>Rainfall</span>
                </td>
                <td className="px-4 py-2.5 font-mono font-bold text-blue-700">35% (0.35)</td>
                <td className="px-4 py-2.5 font-mono">0.0 mm to 200.0 mm</td>
                <td className="px-4 py-2.5 text-slate-600">Linear increase with saturation ceiling at 200mm</td>
              </tr>
              <tr>
                <td className="px-4 py-2.5 font-semibold text-slate-900 flex items-center gap-1.5">
                  <Waves className="w-3.5 h-3.5 text-teal-600" />
                  <span>Tidal Height</span>
                </td>
                <td className="px-4 py-2.5 font-mono font-bold text-blue-700">30% (0.30)</td>
                <td className="px-4 py-2.5 font-mono">0.0 m to 3.0 m</td>
                <td className="px-4 py-2.5 text-slate-600">Astronomical high tide and surge threshold</td>
              </tr>
              <tr>
                <td className="px-4 py-2.5 font-semibold text-slate-900 flex items-center gap-1.5">
                  <Mountain className="w-3.5 h-3.5 text-emerald-600" />
                  <span>Elevation</span>
                </td>
                <td className="px-4 py-2.5 font-mono font-bold text-blue-700">20% (0.20)</td>
                <td className="px-4 py-2.5 font-mono">0.0 m to 20.0 m</td>
                <td className="px-4 py-2.5 text-slate-600">Inverted: 0m = max risk (1.0), &ge;20m = zero risk (0.0)</td>
              </tr>
              <tr>
                <td className="px-4 py-2.5 font-semibold text-slate-900 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />
                  <span>Flood Severity</span>
                </td>
                <td className="px-4 py-2.5 font-mono font-bold text-blue-700">15% (0.15)</td>
                <td className="px-4 py-2.5 font-mono">Discrete category</td>
                <td className="px-4 py-2.5 text-slate-600">None (0.0), Low (0.25), Moderate (0.50), High (0.75), Extreme (1.0)</td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Risk Classification Bounds */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
          <span className="font-bold text-slate-800">Risk Level Classification Thresholds:</span>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1">
            <div className="p-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-900 font-medium">
              Low: &lt; 25.0
            </div>
            <div className="p-2 rounded bg-yellow-50 border border-yellow-200 text-yellow-900 font-medium">
              Moderate: 25.0 to 50.0
            </div>
            <div className="p-2 rounded bg-orange-50 border border-orange-200 text-orange-900 font-medium">
              High: 50.0 to 75.0
            </div>
            <div className="p-2 rounded bg-rose-50 border border-rose-200 text-rose-900 font-medium">
              Critical: &ge; 75.0
            </div>
          </div>
        </div>
      </div>

      {/* ── Data Provenance & Technology Stack ─────────────────────── */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3">
          <div className="flex items-center gap-2">
            <Database className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-slate-900 text-sm">Data Provenance & Ingestion</h3>
          </div>
          <ul className="space-y-2 text-xs text-slate-600">
            <li>
              <strong className="text-slate-800">Weather Provider:</strong> Open-Meteo REST API (precipitation, wind speed, air pressure, temperature).
            </li>
            <li>
              <strong className="text-slate-800">Tidal Provider:</strong> Synthetic Hydrodynamic Simulation Engine (labeled MOCK DATA, not genuine INCOIS telemetry).
            </li>
            <li>
              <strong className="text-slate-800">Terrain Data:</strong> Coastal Topographic Digital Elevation Model (DEM) reference points.
            </li>
            <li>
              <strong className="text-slate-800">Historical Hazard:</strong> Municipal district flood recurrence history records.
            </li>
          </ul>
        </div>

        <div className="p-6 rounded-2xl bg-white border border-slate-200 shadow-xs space-y-3">
          <div className="flex items-center gap-2">
            <Cpu className="w-5 h-5 text-blue-600" />
            <h3 className="font-bold text-slate-900 text-sm">Technology Architecture</h3>
          </div>
          <ul className="space-y-2 text-xs text-slate-600">
            <li>
              <strong className="text-slate-800">Backend:</strong> FastAPI, Python 3.13, Pydantic v2, SQLAlchemy, Tenacity (retry with exponential backoff).
            </li>
            <li>
              <strong className="text-slate-800">Frontend:</strong> React 18, Vite, TypeScript, Tailwind CSS, Recharts, Lucide Icons.
            </li>
            <li>
              <strong className="text-slate-800">Data Persistence:</strong> PostgreSQL 16 with PostGIS spatial extension (with seamless resilient fallback).
            </li>
            <li>
              <strong className="text-slate-800">AI Intelligence:</strong> Local Qwen 3 integration with transparent deterministic reasoning fallback.
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
