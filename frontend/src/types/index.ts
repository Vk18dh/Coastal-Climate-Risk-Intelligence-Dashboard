/**
 * TypeScript Interfaces for Coastal Climate Risk Intelligence Dashboard.
 */

export type RiskLevel = 'Low' | 'Moderate' | 'High' | 'Critical'

export interface RiskEngineResult {
  region_id: number
  timestamp: string
  rainfall_score: number
  tide_score: number
  elevation_score: number
  flood_score: number
  final_score: number | null
  risk_level: RiskLevel | null
  component_scores: Record<string, number>
  original_weights: Record<string, number>
  effective_weights: Record<string, number>
  missing_components: string[]
  data_completeness: number
  warnings: string[]
  methodology_version: string
  status: string
}

export interface RegionCoordinates {
  latitude: number
  longitude: number
}

export interface RegionSummary {
  id: number
  name: string
  district: string
  state?: string
  coast?: string
  elevation_m: number
  flood_severity: string
  description?: string
  coordinates: RegionCoordinates
  latest_risk?: RiskEngineResult
  latest_rainfall_mm?: number
  latest_tide_m?: number
  data_freshness: string
  data_provenance: Record<string, string>
}

export interface RegionDetail extends RegionSummary {
  geojson_polygon?: {
    type: string
    coordinates: number[][][]
  }
  historical_flood_events_count: number
  monitoring_stations: number
}

export interface KPICard {
  title: string
  value: string
  numeric_value?: number
  unit?: string
  status: 'normal' | 'warning' | 'critical' | 'info'
  subtext: string
  icon: string
}

export interface DashboardKPIs {
  overall_risk_score: KPICard
  high_risk_regions: KPICard
  active_alerts: KPICard
  average_rainfall: KPICard
  average_tide: KPICard
  timestamp: string
}

export interface TodaySituation {
  timestamp: string
  overall_classification: string
  overall_score: number
  headline: string
  summary_text: string
  main_contributors: string[]
  active_alerts_count: number
  data_freshness: string
  provenance: Record<string, string>
  methodology_disclosure: string
}

export interface DashboardOverviewResponse {
  kpis: DashboardKPIs
  today_situation: TodaySituation
  regions: RegionSummary[]
}

// ── Analytics ─────────────────────────────────────────────────────────────

export interface Trend {
  first_value: number
  last_value: number
  absolute_change: number
  percentage_change: number | null
}

export interface DescriptiveStats {
  count: number
  min: number | null
  max: number | null
  mean: number | null
  median: number | null
  sample_stddev: number | null
  trend: Trend | null
}

export interface Observation {
  timestamp: string
  value: number
}

export interface TimeSeriesResult {
  metric: string
  observations: Observation[]
  statistics: DescriptiveStats
  provenance: Record<string, string>
  status: string
}

export interface CorrelationResult {
  variable_x: string
  variable_y: string
  correlation: number | null
  paired_observation_count: number
  provenance: Record<string, string>
  status: string
}

export interface RiskDistributionResult {
  region_id: number
  distribution: Record<RiskLevel, number>
  count: number
  provenance: Record<string, string>
  status: string
}

export interface RegionComparison {
  region_id: number
  statistics: DescriptiveStats
  provenance: Record<string, string>
}

export interface ComparisonResult {
  metric: string
  regions: RegionComparison[]
  status: string
}

// ── AI Insights ───────────────────────────────────────────────────────────

export interface AIInsightsResponse {
  region_id: number
  region_name: string
  overall_situation: string
  ccri_score: number
  risk_level: RiskLevel
  main_contributors: string[]
  recommended_actions: string[]
  data_limitations: string[]
  model_status: string
  is_llm_generated: boolean
  llm_executive_briefing?: string
}

export interface AIAskResponse {
  region_id: number
  region_name: string
  question: string
  answer: string
  model_source: string
  disclaimer: string
}

// ── Reports ───────────────────────────────────────────────────────────────

export interface ClimateRiskReport {
  report_id: string
  title: string
  generated_at: string
  region_id: number
  region_name: string
  district: string
  state: string
  elevation_m: number
  current_ccri: RiskEngineResult
  environmental_overview: {
    mean_elevation_meters: number
    historical_flood_severity: string
    latest_rainfall_mm: number
    latest_tide_meters: number
    coastal_orientation: string
  }
  statistical_summary: {
    rainfall_30d: DescriptiveStats
    tide_30d: DescriptiveStats
    risk_30d: DescriptiveStats
  }
  ai_interpretation?: AIInsightsResponse
  recommended_actions: string[]
  provenance: Record<string, string>
  disclaimer: string
  executive_summary: string
}
