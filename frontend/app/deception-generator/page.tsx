"use client";

import { useMemo, useState } from "react";

import { CyberCard } from "@/components/ui/cyber-card";
import { NetworkGraph } from "@/components/visuals/network-graph";
import { useNetworkGraph } from "@/hooks/use-network-graph";
import { useDeceptionData } from "@/hooks/use-deception-data";

export default function DeceptionGeneratorPage() {
  const [density, setDensity] = useState(72);
  const [vulnMode, setVulnMode] = useState("Legacy VPN stack");
  const { graph } = useNetworkGraph();
  const { sessions } = useDeceptionData();

  const credentials = useMemo(
    () => [
      { principal: "svc_backup", credential: "svc_backup@2026!" },
      { principal: "ops-admin", credential: "TempOps#771" },
      { principal: "db_replica", credential: "dbRepl_!490" }
    ],
    []
  );

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-4 space-y-5">
        <CyberCard title="Deception Controls">
          <div className="space-y-4 text-sm text-slate-300">
            <div>
              <label className="mb-1 block text-xs text-slate-400">Infrastructure density</label>
              <input
                type="range"
                min={20}
                max={100}
                value={density}
                onChange={(event) => setDensity(Number(event.target.value))}
                className="w-full accent-cyan-400"
              />
              <p className="mt-1 text-xs text-cyan-200">Density: {density}%</p>
            </div>
            <div>
              <label className="mb-1 block text-xs text-slate-400">Deception scenario</label>
              <select
                value={vulnMode}
                onChange={(event) => setVulnMode(event.target.value)}
                className="w-full rounded-xl border border-cyan-500/20 bg-slate-950/60 px-3 py-2 text-sm text-slate-100"
              >
                <option>Legacy VPN stack</option>
                <option>Unpatched web DMZ</option>
                <option>Hybrid AD takeover bait</option>
              </select>
            </div>
            <div className="grid gap-2">
              {["Inject fake secrets", "Spawn employee personas", "Enable honeyfiles"].map((item) => (
                <label key={item} className="flex items-center gap-2 rounded-lg border border-slate-700 p-2">
                  <input defaultChecked type="checkbox" className="accent-cyan-400" />
                  {item}
                </label>
              ))}
            </div>
          </div>
        </CyberCard>

        <CyberCard title="Active Deception Sessions">
          <div className="space-y-3 text-xs text-slate-300">
            {sessions.map((session) => (
              <div key={session.session_id} className="rounded-lg border border-slate-700/70 bg-slate-950/40 p-3">
                <p className="font-semibold text-cyan-200">{session.attacker_id}</p>
                <p className="text-slate-400">{session.source_ip}</p>
                <p className="text-slate-500">{session.deception_strategy}</p>
              </div>
            ))}
          </div>
        </CyberCard>
      </div>

      <div className="xl:col-span-8 space-y-5">
        <CyberCard title="Adaptive Network Topology">
          <NetworkGraph graph={graph} />
        </CyberCard>

        <CyberCard title="Credential Vault">
          <div className="grid gap-3 md:grid-cols-3">
            {credentials.map((entry) => (
              <div key={entry.principal} className="rounded-lg border border-cyan-500/20 bg-black/40 p-3 text-sm">
                <p className="text-slate-400">{entry.principal}</p>
                <p className="font-mono text-cyan-200">{entry.credential}</p>
              </div>
            ))}
          </div>
        </CyberCard>
      </div>
    </div>
  );
}
