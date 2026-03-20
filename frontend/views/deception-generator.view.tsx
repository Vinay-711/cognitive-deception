"use client";

import { useMemo, useState } from "react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const deceptionNetworkNodes = [
  "edge-gateway-01",
  "legacy-adfs-02",
  "finance-vault-04",
  "iot-gateway-13",
  "fake-hr-portal"
];

const fakeFilesystem = [
  " /",
  " |- home/",
  " |  |- analyst/",
  " |  |- backup/",
  " |- etc/",
  " |  |- ssh/",
  " |  |- ldap.conf",
  " |- var/",
  " |  |- log/",
  " |  |- spool/"
];

const baitPersonas = [
  "Nia Collins (CFO Assistant)",
  "Rohan Mehta (Threat Intel Intern)",
  "Maya Silva (Regional HR)",
  "Lucas Trent (SOC Night Shift)"
];

export function DeceptionGeneratorPage() {
  const [deceptionLevel, setDeceptionLevel] = useState(72);
  const [vulnScenario, setVulnScenario] = useState("Legacy VPN stack");

  const generatedCredentials = useMemo(
    () => [
      { principal: "svc_backup", credential: "svc_backup@2026!" },
      { principal: "ops-admin", credential: "TempOps#771" },
      { principal: "db_replica", credential: "dbRepl_!490" }
    ],
    []
  );

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>Deception Environment Generator</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="mb-1 block text-xs text-slate-400">Generate fake infrastructure density</label>
            <input
              type="range"
              min={20}
              max={100}
              value={deceptionLevel}
              onChange={(event) => setDeceptionLevel(Number(event.target.value))}
              className="w-full accent-cyan-400"
            />
            <p className="mt-1 text-xs text-cyan-200">Density: {deceptionLevel}%</p>
          </div>

          <div>
            <label className="mb-1 block text-xs text-slate-400">Select deception level</label>
            <select
              value={vulnScenario}
              onChange={(event) => setVulnScenario(event.target.value)}
              className="w-full rounded-xl border border-cyan-500/20 bg-slate-950/60 px-3 py-2 text-sm text-slate-100"
            >
              <option>Legacy VPN stack</option>
              <option>Unpatched web DMZ</option>
              <option>Hybrid AD takeover bait</option>
            </select>
          </div>

          <div className="grid gap-2 text-xs">
            {[
              "Simulate vulnerabilities",
              "Inject fake sensitive files",
              "Spawn synthetic employee personas",
              "Enable adaptive credential leakage"
            ].map((item) => (
              <label key={item} className="flex items-center gap-2 rounded-lg border border-slate-700 p-2">
                <input defaultChecked type="checkbox" className="accent-cyan-400" />
                {item}
              </label>
            ))}
          </div>

          <Button className="w-full">Generate Deception Fabric</Button>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>Fake Network Topology</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {deceptionNetworkNodes.map((node, index) => (
            <div key={node} className="flex items-center gap-2 text-xs">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              <span className="font-mono text-cyan-200">{node}</span>
              {index < deceptionNetworkNodes.length - 1 && <span className="text-slate-500">→</span>}
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>Generated Filesystem Tree</CardTitle>
        </CardHeader>
        <CardContent className="space-y-1 font-mono text-xs text-cyan-200">
          {fakeFilesystem.map((line) => (
            <p key={line}>{line}</p>
          ))}
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-6">
        <CardHeader>
          <CardTitle>Fake Credentials Vault</CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {generatedCredentials.map((entry) => (
            <div key={entry.principal} className="rounded-lg border border-cyan-500/20 bg-black/40 p-3 text-sm">
              <p className="text-slate-400">{entry.principal}</p>
              <p className="font-mono text-cyan-200">{entry.credential}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-6">
        <CardHeader>
          <CardTitle>Email / Social Engineering Bait Personas</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-2">
          {baitPersonas.map((persona) => (
            <div key={persona} className="rounded-lg border border-violet-500/20 bg-violet-500/5 p-3 text-sm text-violet-200">
              {persona}
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
