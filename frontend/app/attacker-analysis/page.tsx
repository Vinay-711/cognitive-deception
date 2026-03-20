"use client";

import { useMemo } from "react";

import { CyberCard } from "@/components/ui/cyber-card";
import { AttackTimeline } from "@/components/visuals/attack-timeline";
import { useAttackFeed } from "@/hooks/use-attack-feed";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

export default function AttackerAnalysisPage() {
  const { events } = useAttackFeed();
  const { metrics, topAttackerType } = usePlatformMetrics();

  const biasEntries = useMemo(() => {
    const biasCounts = metrics?.bias_counts ?? {
      overconfidence: 30,
      confirmation_bias: 21,
      time_pressure: 15,
      recon_pattern: 8
    };
    const max = Math.max(...Object.values(biasCounts));
    return Object.entries(biasCounts).map(([bias, value]) => ({
      bias,
      value,
      width: max ? Math.round((value / max) * 100) : 0
    }));
  }, [metrics]);

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-5 space-y-5">
        <CyberCard title="Attacker Cognitive Profile">
          <div className="space-y-4 text-sm text-slate-300">
            <div>
              <p className="text-xs text-slate-400">Likely actor class</p>
              <p className="mt-1 text-lg font-semibold text-cyan-100">{topAttackerType}</p>
            </div>
            <div>
              <p className="text-xs text-slate-400">Skill level prediction</p>
              <p className="mt-1 text-lg font-semibold text-violet-200">Advanced Operator</p>
            </div>
            <div>
              <p className="text-xs text-slate-400">Typing pattern analysis</p>
              <p className="mt-1 text-slate-300">Rapid multi-command bursts · 210ms mean latency</p>
            </div>
          </div>
        </CyberCard>

        <CyberCard title="Detected Cognitive Biases">
          <div className="space-y-3">
            {biasEntries.map((entry) => (
              <div key={entry.bias}>
                <div className="flex items-center justify-between text-xs text-slate-400">
                  <span>{entry.bias.replace(/_/g, " ")}</span>
                  <span className="text-cyan-200">{entry.value}</span>
                </div>
                <div className="mt-1 h-2 w-full rounded-full bg-slate-900">
                  <div
                    className="h-2 rounded-full bg-gradient-to-r from-violet-400 to-cyan-300"
                    style={{ width: `${entry.width}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CyberCard>
      </div>

      <div className="xl:col-span-7 space-y-5">
        <CyberCard title="Command Sequence Graph">
          <div className="min-h-[16rem] rounded-2xl border border-cyan-500/20 bg-[radial-gradient(circle_at_20%_20%,rgba(0,229,255,.08),transparent_45%),#05070a] p-6 text-xs text-slate-400">
            <p className="mb-4 text-sm text-cyan-200">Sequence inference (last 10 commands)</p>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {events.slice(0, 10).map((event, idx) => (
                <div key={`${event.session_id}-${idx}`} className="flex flex-col rounded-lg border border-slate-800 bg-black/40 p-2 overflow-hidden">
                  <p className="text-cyan-200">{idx + 1}</p>
                  <p className="mt-1 font-mono text-[10px] text-slate-400 break-all">{event.command}</p>
                </div>
              ))}
            </div>
          </div>
        </CyberCard>

        <CyberCard title="Behavior Timeline">
          <AttackTimeline events={events} />
        </CyberCard>
      </div>
    </div>
  );
}
