"use client";

import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  PolarAngleAxis,
  PolarGrid,
  Radar,
  RadarChart,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

const attackerSkillRadar = [
  { metric: "Recon", score: 88 },
  { metric: "Stealth", score: 72 },
  { metric: "Exploit", score: 79 },
  { metric: "Persistence", score: 64 },
  { metric: "Exfil", score: 83 }
];
const behaviorTimeline = [
  { step: "T+0", entropy: 20, aggression: 25 },
  { step: "T+5", entropy: 42, aggression: 47 },
  { step: "T+10", entropy: 61, aggression: 59 },
  { step: "T+15", entropy: 57, aggression: 72 },
  { step: "T+20", entropy: 73, aggression: 80 }
];
const behaviorClusters = [
  { x: 2, y: 8, z: 94, group: "Brute" },
  { x: 6, y: 5, z: 82, group: "Recon" },
  { x: 8, y: 3, z: 75, group: "Exploit" },
  { x: 7, y: 9, z: 88, group: "Exfil" },
  { x: 4, y: 4, z: 57, group: "Low-Signal" }
];

export function AttackerProfilePage() {
  const { metrics } = usePlatformMetrics();
  const cognitiveBiasScores = metrics?.cognitive_bias_scores || [];
  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <Card className="p-4 xl:col-span-12">
        <CardHeader>
          <CardTitle>Attacker Cognitive Profile</CardTitle>
          <Badge variant="purple">Attacker ID: APT-9071</Badge>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-4">
          <div className="rounded-xl border border-cyan-500/20 bg-black/40 p-3">
            <p className="text-xs text-slate-400">Skill Level Prediction</p>
            <p className="mt-1 text-xl font-semibold text-cyan-100">Advanced</p>
          </div>
          <div className="rounded-xl border border-cyan-500/20 bg-black/40 p-3">
            <p className="text-xs text-slate-400">Typing Pattern</p>
            <p className="mt-1 text-xl font-semibold text-cyan-100">Burst + Delay</p>
          </div>
          <div className="rounded-xl border border-cyan-500/20 bg-black/40 p-3">
            <p className="text-xs text-slate-400">Behavior Volatility</p>
            <p className="mt-1 text-xl font-semibold text-cyan-100">0.73</p>
          </div>
          <div className="rounded-xl border border-cyan-500/20 bg-black/40 p-3">
            <p className="text-xs text-slate-400">Current Bias</p>
            <p className="mt-1 text-xl font-semibold text-violet-300">Overconfidence</p>
          </div>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>Cognitive Bias Radar</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={attackerSkillRadar}>
              <PolarGrid stroke="rgba(148,163,184,.22)" />
              <PolarAngleAxis dataKey="metric" tick={{ fill: "#9ca3af", fontSize: 12 }} />
              <Radar name="Skill" dataKey="score" stroke="#00E5FF" fill="#00E5FF" fillOpacity={0.28} />
            </RadarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>Behavior Timeline</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={behaviorTimeline}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.15)" />
              <XAxis dataKey="step" tick={{ fill: "#9ca3af", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={26} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="entropy" stroke="#00E5FF" strokeWidth={2} dot={false} />
              <Line type="monotone" dataKey="aggression" stroke="#FF3B3B" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-4">
        <CardHeader>
          <CardTitle>TTP Correlation Graph</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.15)" />
              <XAxis type="number" dataKey="x" name="Stealth" tick={{ fill: "#9ca3af", fontSize: 11 }} />
              <YAxis type="number" dataKey="y" name="Aggression" tick={{ fill: "#9ca3af", fontSize: 11 }} />
              <Tooltip cursor={{ strokeDasharray: "3 3" }} />
              <Scatter name="Behavior cluster" data={behaviorClusters} fill="#7C4DFF" />
            </ScatterChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-12">
        <CardHeader>
          <CardTitle>Detected Cognitive Biases</CardTitle>
        </CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-4">
          {cognitiveBiasScores.map((item) => (
            <div key={item.bias} className="rounded-xl border border-violet-500/20 bg-violet-500/5 p-3">
              <p className="text-xs text-slate-400">{item.bias}</p>
              <p className="mt-1 text-lg font-semibold text-violet-200">{item.score}% signal</p>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
}
