import React from 'react';
import { FileText, Download, FileSpreadsheet } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100">Climate Reports & Exports</h1>
        <p className="text-slate-400 text-sm mt-1">
          Downloadable Executive Summaries, PDF Briefings & CSV Datasets
        </p>
      </div>

      <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center min-h-[400px] text-center space-y-4">
        <div className="p-4 bg-emerald-500/10 text-emerald-400 rounded-full border border-emerald-500/20">
          <FileText className="w-10 h-10" />
        </div>
        <div className="max-w-md space-y-2">
          <h3 className="text-lg font-semibold text-slate-200">Report Generator Foundation Wired</h3>
          <p className="text-sm text-slate-400">
            ReportLab PDF export engine and CSV serialiser boundaries established. Automated report generation scheduled for Sprint 3.
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs font-mono bg-slate-950 px-3 py-1.5 rounded border border-slate-800 text-slate-400">
          <Download className="w-3.5 h-3.5 text-emerald-400" />
          <span>Endpoint: /api/v1/reports</span>
        </div>
      </div>
    </div>
  );
};
