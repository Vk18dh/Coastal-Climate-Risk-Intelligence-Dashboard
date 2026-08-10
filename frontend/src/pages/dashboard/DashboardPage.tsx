import React, { useEffect, useState } from 'react';
import { apiClient } from '../../services/apiClient';
import { Activity, Server, Database, CheckCircle2 } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const [healthData, setHealthData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    apiClient.get('/health')
      .then((res) => {
        setHealthData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Health fetch failed:', err);
        setLoading(false);
      });
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Coastal Climate Risk Dashboard</h1>
        <p className="text-slate-400 text-sm mt-1">
          AI-Powered Decision Support System Foundation
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-sky-500/10 text-sky-400 rounded-lg">
              <Server className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">FastAPI Backend</p>
              <p className="text-sm font-semibold text-slate-200 mt-0.5">
                {loading ? 'Connecting...' : healthData?.success ? 'Active' : 'Offline'}
              </p>
            </div>
          </div>
        </div>

        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">PostGIS Database</p>
              <p className="text-sm font-semibold text-slate-200 mt-0.5">
                {healthData?.data?.database_connected ? 'Connected' : 'Standalone Mode'}
              </p>
            </div>
          </div>
        </div>

        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-purple-500/10 text-purple-400 rounded-lg">
              <Activity className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xs font-medium text-slate-400">System Wired</p>
              <p className="text-sm font-semibold text-slate-200 mt-0.5">Sprint 1 Foundation</p>
            </div>
          </div>
        </div>
      </div>

      <div className="p-6 bg-slate-900/60 border border-slate-800 rounded-xl">
        <h2 className="text-lg font-semibold text-slate-200 flex items-center space-x-2">
          <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          <span>System Infrastructure Wiring Complete</span>
        </h2>
        <p className="text-sm text-slate-400 mt-2">
          The foundation layer has established configuration, routing, and backend communication. Data ingestion and predictive analytics will be populated in subsequent sprints.
        </p>
      </div>
    </div>
  );
};
