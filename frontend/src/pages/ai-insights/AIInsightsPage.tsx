import { useState } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import { apiService } from '@/services/api'
import { useAppStore } from '@/store/useAppStore'
import {
  Bot,
  Send,
  Sparkles,
  ShieldAlert,
  AlertCircle,
  CheckCircle2,
  Info,
  MapPin,
  RefreshCw,
} from 'lucide-react'

export default function AIInsightsPage() {
  const { selectedRegionId, setSelectedRegionId } = useAppStore()
  const [questionText, setQuestionText] = useState('')
  const [chatHistory, setChatHistory] = useState<Array<{ q: string; a: string; model: string }>>([])

  // Fetch Regions list
  const { data: regions } = useQuery({
    queryKey: ['regions'],
    queryFn: () => apiService.getRegions(),
  })

  // Fetch AI Insights for selected region
  const { data: insights, isLoading, refetch } = useQuery({
    queryKey: ['ai-insights', selectedRegionId],
    queryFn: () => apiService.getAIInsights(selectedRegionId),
  })

  // Ask Question Mutation
  const askMutation = useMutation({
    mutationFn: (q: string) => apiService.askAI(selectedRegionId, q),
    onSuccess: (data) => {
      setChatHistory((prev) => [
        ...prev,
        { q: data.question, a: data.answer, model: data.model_source },
      ])
      setQuestionText('')
    },
  })

  const currentRegion = regions?.find((r) => r.id === selectedRegionId)

  const handleAsk = (q?: string) => {
    const query = q || questionText
    if (!query.trim() || askMutation.isPending) return
    askMutation.mutate(query.trim())
  }

  const QUICK_QUESTIONS = [
    'Why is this region at risk?',
    'What emergency actions should be considered?',
    'How does tide height impact this zone?',
    'What is the topographic elevation risk?',
  ]

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-sm font-medium text-slate-600">Generating grounded AI insights...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-10">
      {/* ── Page Header ────────────────────────────────────────────── */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-200 pb-4">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <Bot className="w-6 h-6 text-blue-600" />
            <span>AI Climate Intelligence & Decision Support</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Deterministic risk interpretation, environmental contributor attribution & automated advisory synthesis
          </p>
        </div>

        {/* Region Selector */}
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
                  {r.name} ({r.district})
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={() => refetch()}
            className="p-2 rounded-lg bg-white border border-slate-200 text-slate-600 hover:bg-slate-50 transition-colors shadow-xs"
            title="Refresh Insights"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* ── Model Transparency Header Card ─────────────────────────── */}
      <div className="bg-slate-900 text-slate-100 rounded-2xl p-5 shadow-sm border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-blue-600/30 border border-blue-500/40 flex items-center justify-center text-blue-400">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-bold text-white">Active Reasoning Engine:</span>
              <span className="text-xs font-mono px-2 py-0.5 rounded bg-blue-950 text-blue-300 border border-blue-800">
                {insights?.model_status || 'Grounded Deterministic Engine'}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Strictly grounded in Phase 5 CCRI parameters · Never hallucinates external telemetry
            </p>
          </div>
        </div>

        <div className="text-right">
          <span className="text-xs text-slate-400">Selected Zone:</span>
          <p className="text-sm font-bold text-white">{currentRegion?.name}</p>
        </div>
      </div>

      {/* ── Grid: Situation, Contributors, Actions ──────────────────── */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        {/* Left Side: Structured Assessment (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          {/* Section 1: Overall Situation */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <h2 className="text-sm font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-blue-600" />
                <span>Executive Situation Overview</span>
              </h2>
              <span className="text-xs font-bold px-2.5 py-0.5 rounded-full bg-slate-100 text-slate-700">
                CCRI {insights?.ccri_score?.toFixed(1)}/100 · {insights?.risk_level} Risk
              </span>
            </div>
            <p className="text-sm text-slate-700 leading-relaxed font-medium">
              {insights?.overall_situation}
            </p>
          </div>

          {/* Section 2: Main Risk Contributors */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-3">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-amber-600" />
              <span>Primary Risk Contributors & Physical Drivers</span>
            </h2>
            <div className="space-y-2.5">
              {insights?.main_contributors.map((c, idx) => (
                <div key={idx} className="p-3 rounded-lg bg-slate-50 border border-slate-200 text-xs text-slate-700">
                  <span className="font-semibold text-slate-900">{c.split(':')[0]}:</span>
                  <span className="ml-1 text-slate-600">{c.split(':')[1] || c}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section 3: Recommended Actions */}
          <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs space-y-3">
            <h2 className="text-sm font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              <span>Operational Precautionary Recommendations</span>
            </h2>
            <ul className="space-y-2 text-xs text-slate-700">
              {insights?.recommended_actions.map((action, idx) => (
                <li key={idx} className="flex items-start gap-2.5 p-2 rounded-lg hover:bg-slate-50 transition-colors">
                  <span className="w-5 h-5 rounded-full bg-emerald-100 text-emerald-700 font-bold flex items-center justify-center flex-shrink-0 text-[11px]">
                    {idx + 1}
                  </span>
                  <span className="leading-relaxed mt-0.5">{action}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Section 4: Data Limitations Disclosure */}
          <div className="bg-amber-50 rounded-2xl border border-amber-200 p-5 space-y-2">
            <div className="flex items-center gap-2 text-amber-900 font-bold text-xs uppercase tracking-wider">
              <Info className="w-4 h-4 text-amber-700" />
              <span>Methodology & Data Limitations Disclosure</span>
            </div>
            <ul className="space-y-1 text-xs text-amber-800">
              {insights?.data_limitations.map((limit, idx) => (
                <li key={idx} className="flex items-start gap-2">
                  <span>•</span>
                  <span>{limit}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Right Side: Interactive AI Assistant (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col h-[640px]">
          {/* Chat Header */}
          <div className="p-4 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-slate-900">Coastal Risk AI Assistant</h3>
                <p className="text-[10px] text-slate-500">Grounded in {currentRegion?.name} telemetry</p>
              </div>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-medium">
              Ready
            </span>
          </div>

          {/* Chat Messages Feed */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 text-xs">
            {/* Introductory greeting */}
            <div className="bg-slate-100 text-slate-800 p-3 rounded-xl rounded-tl-none space-y-1">
              <p className="font-semibold text-slate-900">
                Hello. I am the Coastal Climate Risk Intelligence Assistant for {currentRegion?.name}.
              </p>
              <p className="text-slate-600">
                You can ask me to explain why this region is evaluated at {insights?.risk_level} risk,
                detail contributing factors, or recommend emergency actions.
              </p>
            </div>

            {/* Quick Prompt Chips */}
            <div className="space-y-1.5 pt-1">
              <p className="text-[10px] font-bold uppercase tracking-wider text-slate-400">
                Suggested Questions:
              </p>
              <div className="flex flex-col gap-1.5">
                {QUICK_QUESTIONS.map((q, idx) => (
                  <button
                    key={idx}
                    onClick={() => handleAsk(q)}
                    className="text-left px-3 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-blue-50 hover:border-blue-200 text-slate-700 text-xs transition-colors"
                  >
                    &ldquo;{q}&rdquo;
                  </button>
                ))}
              </div>
            </div>

            {/* User Interaction History */}
            {chatHistory.map((item, idx) => (
              <div key={idx} className="space-y-2 pt-2">
                {/* User message */}
                <div className="flex justify-end">
                  <div className="bg-blue-600 text-white p-3 rounded-xl rounded-tr-none max-w-[85%] font-medium">
                    {item.q}
                  </div>
                </div>

                {/* AI response */}
                <div className="flex justify-start">
                  <div className="bg-slate-100 text-slate-800 p-3.5 rounded-xl rounded-tl-none max-w-[90%] space-y-1.5 leading-relaxed">
                    <p className="whitespace-pre-line text-slate-800">{item.a}</p>
                    <div className="pt-1.5 border-t border-slate-200 text-[10px] text-slate-500 font-mono">
                      Source: {item.model}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {askMutation.isPending && (
              <div className="flex items-center gap-2 text-slate-500 text-xs italic p-2">
                <div className="w-3.5 h-3.5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <span>Analyzing environmental risk parameters...</span>
              </div>
            )}
          </div>

          {/* Chat Input Bar */}
          <div className="p-3 border-t border-slate-200 bg-slate-50">
            <form
              onSubmit={(e) => {
                e.preventDefault()
                handleAsk()
              }}
              className="flex items-center gap-2"
            >
              <input
                type="text"
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                placeholder={`Ask about ${currentRegion?.name.split(' ')[0]}'s risk...`}
                className="flex-1 text-xs px-3 py-2 bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-900"
              />
              <button
                type="submit"
                disabled={!questionText.trim() || askMutation.isPending}
                className="p-2 rounded-lg bg-blue-600 hover:bg-blue-700 text-white disabled:opacity-50 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  )
}
