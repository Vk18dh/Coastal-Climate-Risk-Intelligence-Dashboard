import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Layout } from '../components/layout/Layout';
import { DashboardPage } from '../pages/dashboard/DashboardPage';
import { RiskMapPage } from '../pages/risk/RiskMapPage';
import { AnalyticsPage } from '../pages/analytics/AnalyticsPage';
import { AIInsightsPage } from '../pages/ai/AIInsightsPage';
import { ReportsPage } from '../pages/reports/ReportsPage';
import { AboutPage } from '../pages/about/AboutPage';

export const AppRoutes: React.FC = () => {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/risk-map" element={<RiskMapPage />} />
        <Route path="/analytics" element={<AnalyticsPage />} />
        <Route path="/ai-insights" element={<AIInsightsPage />} />
        <Route path="/reports" element={<ReportsPage />} />
        <Route path="/about" element={<AboutPage />} />
      </Routes>
    </Layout>
  );
};
