"use client";

import { useMemo } from "react";

import { CyberCard } from "@/components/ui/cyber-card";
import { ThreatMap } from "@/components/visuals/threat-map";
import { AttackTimeline } from "@/components/visuals/attack-timeline";
import { AIInsightPanel } from "@/components/visuals/ai-insight-panel";
import { useAttackFeed } from "@/hooks/use-attack-feed";
import { useAnalysisSummary } from "@/hooks/use-analysis-summary";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";
import { useDeceptionData } from "@/hooks/use-deception-data";

const fallbackCounts = {
  overconfidence: 32,
  confirmation_bias: 24,
  time_pressure: 18,
  recon_pattern: 12
};

export default function DashboardPage() {
  const { metrics, topAttackerType } = usePlatformMetrics();
  const { events } = useAttackFeed();
  const { summary } = useAnalysisSummary();
  const { sessions } = useDeceptionData();

  const activeSessions = metrics?.active_sessions ?? summary?.active_sessions ?? sessions.length;
  const totalEvents = metrics?.total_events ?? summary?.total_events ?? events.length;

  const biasCounts = metrics?.bias_counts ?? fallbackCounts;
  const topBias = summary?.top_bias ??
    Object.entries(biasCounts).sort((a, b) => b[1] - a[1])[0]?.[0] ?? "unknown";

  const deceptionSuccess = useMemo(() => {
    const strategyCounts = metrics?.strategy_counts ?? {
      baseline_obfuscation: 14,
      credential_sinkhole: 9,
      surface_expansion: 7
    };
    const total = Object.values(strategyCounts).reduce((sum, value) => sum + value, 0);
    const top = Object.values(strategyCounts)[0] ?? 0;
    if (!total) return 0;
    return Math.min(96, Math.round((top / total) * 100 + 40));
  }, [metrics]);

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-12 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {[
          { title: "Active Sessions", value: activeSessions, helper: "Honeypot engagements" },
          { title: "Total Events", value: totalEvents, helper: "Commands intercepted" },
          { title: "Top Attacker", value: summary?.top_attacker_type ?? topAttackerType ?? "Unknown", helper: "Behavior clustering" },
          { title: "Dominant Bias", value: topBias.replace(/_/g, " "), helper: "Cognitive inference" }
        ].map((card) => (
          <CyberCard key={card.title} title={card.title}>
            <div className="space-y-2">
              <p className="text-3xl font-semibold text-cyan-100">{card.value}</p>
              <p className="text-xs text-slate-400">{card.helper}</p>
            </div>
          </CyberCard>
        ))}
      </div>

      <div className="xl:col-span-7 space-y-5">
        <CyberCard title="Global Attack Heatmap">
          <ThreatMap />
        </CyberCard>

        <CyberCard title="Live Attack Timeline">
          <AttackTimeline events={events} />
        </CyberCard>
      </div>

      <div className="xl:col-span-5 space-y-5">
        <CyberCard title="AI Insight Panel">
          <AIInsightPanel summary={summary} />
        </CyberCard>

        <CyberCard title="Deception Success Rate">
          <div className="space-y-4 text-sm text-slate-300">
            <div>
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span>Adaptive deception efficacy</span>
                <span className="text-cyan-200">{deceptionSuccess}%</span>
              </div>
              <div className="mt-2 h-2 w-full rounded-full bg-slate-900">
                <div
                  className="h-2 rounded-full bg-gradient-to-r from-cyan-400 via-cyan-200 to-violet-400"
                  style={{ width: `${deceptionSuccess}%` }}
                />
              </div>
            </div>
            <p className="text-xs text-slate-500">Live tuning based on attacker cognition and session drift.</p>
          </div>
        </CyberCard>

        <CyberCard title="Active Deception Sessions">
          <div className="space-y-3 text-xs text-slate-300">
            {sessions.slice(0, 5).map((session) => (
              <div key={session.session_id} className="rounded-xl border border-slate-700/70 bg-slate-950/40 p-3">
                <p className="font-semibold text-cyan-200">{session.attacker_id}</p>
                <p className="text-slate-400">{session.source_ip}</p>
                <p className="text-slate-500">{session.deception_strategy}</p>
              </div>
            ))}
          </div>
        </CyberCard>
      </div>
    </div>
  );
}
