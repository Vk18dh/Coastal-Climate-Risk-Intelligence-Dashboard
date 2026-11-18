import apiClient from '@/config/api'
import type {
  AIAskResponse,
  AIInsightsResponse,
  ClimateRiskReport,
  ComparisonResult,
  CorrelationResult,
  DashboardOverviewResponse,
  RegionDetail,
  RegionSummary,
  RiskDistributionResult,
  TimeSeriesResult,
} from '@/types'

export const apiService = {
  // ── Dashboard & Regions ──────────────────────────────────────────────────
  async getDashboard(): Promise<DashboardOverviewResponse> {
    const res = await apiClient.get<DashboardOverviewResponse>('/dashboard')
    return res.data
  },

  async getRegions(): Promise<RegionSummary[]> {
    const res = await apiClient.get<RegionSummary[]>('/regions')
    return res.data
  },

  async getRegion(regionId: number): Promise<RegionDetail> {
    const res = await apiClient.get<RegionDetail>(`/regions/${regionId}`)
    return res.data
  },

  async getGeoJson(): Promise<any> {
    const res = await apiClient.get('/maps/geojson')
    return res.data
  },

  // ── Analytics ────────────────────────────────────────────────────────────
  async getTimeseries(
    regionId: number,
    metric: string,
    days: number = 30
  ): Promise<TimeSeriesResult> {
    const res = await apiClient.get<TimeSeriesResult>('/analytics/timeseries', {
      params: { region_id: regionId, metric, days },
    })
    return res.data
  },

  async getCorrelation(
    regionId: number,
    variableX: string,
    variableY: string,
    days: number = 30
  ): Promise<CorrelationResult> {
    const res = await apiClient.get<CorrelationResult>('/analytics/correlation', {
      params: { region_id: regionId, variable_x: variableX, variable_y: variableY, days },
    })
    return res.data
  },

  async getRiskDistribution(
    regionId: number,
    days: number = 30
  ): Promise<RiskDistributionResult> {
    const res = await apiClient.get<RiskDistributionResult>('/analytics/distribution', {
      params: { region_id: regionId, days },
    })
    return res.data
  },

  async getComparison(metric: string, days: number = 30): Promise<ComparisonResult> {
    const res = await apiClient.get<ComparisonResult>('/analytics/comparison', {
      params: { metric, days },
    })
    return res.data
  },

  // ── AI Insights ──────────────────────────────────────────────────────────
  async getAIInsights(regionId: number): Promise<AIInsightsResponse> {
    const res = await apiClient.get<AIInsightsResponse>(`/ai/regions/${regionId}/insights`)
    return res.data
  },

  async askAI(regionId: number, question: string): Promise<AIAskResponse> {
    const res = await apiClient.post<AIAskResponse>('/ai/ask', {
      region_id: regionId,
      question,
    })
    return res.data
  },

  // ── Reports ──────────────────────────────────────────────────────────────
  async generateReport(
    regionId: number,
    includeAi: boolean = true,
    includeTrends: boolean = true
  ): Promise<ClimateRiskReport> {
    const res = await apiClient.post<ClimateRiskReport>('/reports/generate', {
      region_id: regionId,
      include_ai_insights: includeAi,
      include_statistical_trends: includeTrends,
    })
    return res.data
  },

  async getReports(): Promise<ClimateRiskReport[]> {
    const res = await apiClient.get<ClimateRiskReport[]>('/reports')
    return res.data
  },

  async getReport(reportId: string): Promise<ClimateRiskReport> {
    const res = await apiClient.get<ClimateRiskReport>(`/reports/${reportId}`)
    return res.data
  },
}

