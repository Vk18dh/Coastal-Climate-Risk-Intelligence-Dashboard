import React from 'react';
import { MapPin, Layers, Globe } from 'lucide-react';

export const RiskMapPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Interactive GIS Risk Map</h1>
        <p className="text-slate-400 text-sm mt-1">
          Geospatial Coastal Zone Mapping & Vulnerability Layers (OpenFreeMap + Leaflet Infrastructure)
        </p>
      </div>

      <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center min-h-[400px] text-center space-y-4">
        <div className="p-4 bg-sky-500/10 text-sky-400 rounded-full border border-sky-500/20">
          <Globe className="w-10 h-10 animate-spin-slow" />
        </div>
        <div className="max-w-md space-y-2">
          <h3 className="text-lg font-semibold text-slate-200">GIS Mapping Container Ready</h3>
          <p className="text-sm text-slate-400">
            OpenFreeMap vector tile provider & Leaflet routing infrastructure wired. PostGIS geospatial polygon queries will populate regional risk layers in Sprint 2.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-950 px-3 py-1.5 rounded border border-slate-800 text-slate-400">
          <MapPin className="w-3.5 h-3.5 text-sky-400" />
          <span>Endpoint: /api/v1/regions</span>
        </div>
      </div>
    </div>
  );
};
