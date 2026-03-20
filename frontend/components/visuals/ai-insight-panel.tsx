"use client";

import { type AnalysisSummary } from "@/services/api-client";

export function AIInsightPanel({ summary }: { summary: AnalysisSummary | null }) {
  return (
    <div className="space-y-3">
      <div className="rounded-xl border border-violet-500/20 bg-violet-500/5 p-3">
        <p className="text-xs text-slate-400">Top Attacker Type</p>
        <p className="mt-1 text-lg font-semibold text-violet-200">{summary?.top_attacker_type ?? "unknown"}</p>
      </div>
      <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-3">
        <p className="text-xs text-slate-400">Dominant Bias</p>
        <p className="mt-1 text-lg font-semibold text-cyan-200">{summary?.top_bias ?? "unknown"}</p>
      </div>
      <div className="rounded-xl border border-slate-700/70 bg-slate-950/40 p-3 text-xs text-slate-400">
        Active sessions: {summary?.active_sessions ?? 0} · Total events: {summary?.total_events ?? 0}
      </div>
    </div>
  );
}
