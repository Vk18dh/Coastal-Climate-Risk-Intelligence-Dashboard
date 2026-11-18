import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardPage from '@/pages/dashboard/DashboardPage'
import RiskMapPage from '@/pages/risk/RiskMapPage'
import AnalyticsPage from '@/pages/analytics/AnalyticsPage'
import AIInsightsPage from '@/pages/ai-insights/AIInsightsPage'
import ReportsPage from '@/pages/reports/ReportsPage'
import AboutPage from '@/pages/about/AboutPage'

/**
 * Application route map.
 *
 * All routes are rendered inside AppLayout (sidebar + main content area).
 * Unknown paths redirect to the Dashboard.
 */
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<DashboardPage />} />
      <Route path="/risk-map" element={<RiskMapPage />} />
      <Route path="/analytics" element={<AnalyticsPage />} />
      <Route path="/ai-insights" element={<AIInsightsPage />} />
      <Route path="/reports" element={<ReportsPage />} />
      <Route path="/about" element={<AboutPage />} />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
