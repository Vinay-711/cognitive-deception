"use client";

import { CyberCard } from "@/components/ui/cyber-card";
import { ThreatMap } from "@/components/visuals/threat-map";
import { useAnalysisSummary } from "@/hooks/use-analysis-summary";

const fallbackHeat = [
  { technique: "T1046 Network Service Scanning", intensity: 0.84 },
  { technique: "T1110 Credential Brute Force", intensity: 0.72 },
  { technique: "T1021 Remote Services", intensity: 0.63 }
];

export default function ThreatIntelligencePage() {
  const { summary } = useAnalysisSummary();
  const heat = summary?.mitre_heat?.length ? summary.mitre_heat : fallbackHeat;

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-7 space-y-5">
        <CyberCard title="MITRE ATT&CK Mapping">
          <div className="space-y-3">
            {heat.map((entry) => {
              const maxIntensity = Math.max(...heat.map(e => e.intensity), 1);
              const percentage = Math.min(Math.round((entry.intensity / maxIntensity) * 100), 100);
              return (
                <div key={entry.technique} className="rounded-xl border border-slate-800 bg-slate-950/40 p-3">
                  <div className="flex items-center justify-between text-xs text-slate-400">
                    <span>{entry.technique}</span>
                    <span className="text-cyan-200">{entry.intensity > 1 ? entry.intensity : Math.round(entry.intensity * 100)}%</span>
                  </div>
                  <div className="mt-2 h-2 w-full rounded-full bg-slate-900">
                    <div
                      className="h-2 rounded-full bg-gradient-to-r from-cyan-400 to-red-400"
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </CyberCard>

        <CyberCard title="Threat Intelligence Feed">
          <ul className="space-y-3 text-sm text-slate-300">
            {[
              "Credential harvesting attempts rising in APAC",
              "Observed persistence via cron injection",
              "Lateral movement detected against honeyfile shares"
            ].map((item) => (
              <li key={item} className="rounded-lg border border-slate-800 bg-black/40 p-3">
                {item}
              </li>
            ))}
          </ul>
        </CyberCard>
      </div>

      <div className="xl:col-span-5 space-y-5">
        <CyberCard title="Global Threat Distribution">
          <ThreatMap />
        </CyberCard>

        <CyberCard title="AI Threat Assessment">
          <div className="space-y-3 text-sm text-slate-300">
            <p>High confidence that actor is probing adaptive honeypot infrastructure.</p>
            <p className="text-xs text-slate-500">Recommendation: keep deception layer in aggressive mode for next 30 minutes.</p>
          </div>
        </CyberCard>
      </div>
    </div>
  );
}
