import React from 'react';
import { Info, Layers, Code2, Server } from 'lucide-react';

export const AboutPage: React.FC = () => {
  return (
    <div className="space-y-6 max-w-4xl">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">About the Platform</h1>
        <p className="text-slate-400 text-sm mt-1">
          AI-Powered Geospatial Decision Support System for Coastal Climate Risk Assessment
        </p>
      </div>

      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl space-y-4">
        <h2 className="text-lg font-semibold text-slate-200">System Architecture & Tech Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800">
            <h3 className="font-semibold text-sky-400 flex items-center space-x-2">
              <Server className="w-4 h-4" />
              <span>Backend & Infrastructure</span>
            </h3>
            <ul className="mt-2 space-y-1 text-slate-400 text-xs">
              <li>• FastAPI (Python 3.11+)</li>
              <li>• PostgreSQL + PostGIS Extension</li>
              <li>• SQLAlchemy 2.0 ORM + Alembic</li>
              <li>• Redis Caching Layer</li>
            </ul>
          </div>

          <div className="p-4 bg-slate-950/60 rounded-lg border border-slate-800">
            <h3 className="font-semibold text-purple-400 flex items-center space-x-2">
              <Code2 className="w-4 h-4" />
              <span>Frontend & GIS</span>
            </h3>
            <ul className="mt-2 space-y-1 text-slate-400 text-xs">
              <li>• React 18 + Vite + TypeScript</li>
              <li>• Tailwind CSS Styling</li>
              <li>• OpenFreeMap + Leaflet / MapLibre GL</li>
              <li>• Recharts Statistical Visualization</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};
