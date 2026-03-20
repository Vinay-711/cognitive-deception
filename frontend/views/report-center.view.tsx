"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  PolarAngleAxis,
  PolarGrid,
  RadialBar,
  RadialBarChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis
} from "recharts";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const killChainSeries = [
  { phase: "Recon", completion: 92 },
  { phase: "Weaponization", completion: 70 },
  { phase: "Delivery", completion: 65 },
  { phase: "Exploitation", completion: 81 },
  { phase: "Exfiltration", completion: 48 }
];

const behaviorClusters = [
  { x: 2, y: 8, z: 94, group: "Brute" },
  { x: 6, y: 5, z: 82, group: "Recon" },
  { x: 8, y: 3, z: 75, group: "Exploit" },
  { x: 7, y: 9, z: 88, group: "Exfil" },
  { x: 4, y: 4, z: 57, group: "Low-Signal" }
];

export function ReportCenterPage() {
  const successProbability = [{ name: "Success", value: 78, fill: "#00E5FF" }];

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <Card className="p-4 xl:col-span-12">
        <CardHeader>
          <CardTitle>Intelligence Report Center</CardTitle>
        </CardHeader>
        <CardContent className="flex flex-wrap gap-3">
          <Button>Export Threat Intelligence</Button>
          <Button variant="ghost">Generate MITRE ATT&CK PDF</Button>
          <Button variant="ghost">Behavioral Insight Summary</Button>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-7">
        <CardHeader>
          <CardTitle>Kill Chain Progression</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={killChainSeries}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.15)" />
              <XAxis dataKey="phase" tick={{ fill: "#9ca3af", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={28} />
              <Tooltip />
              <Bar dataKey="completion" fill="#7C4DFF" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-5">
        <CardHeader>
          <CardTitle>Attack Success Probability</CardTitle>
        </CardHeader>
        <CardContent className="h-[300px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadialBarChart innerRadius="55%" outerRadius="95%" barSize={22} data={successProbability}>
              <PolarGrid gridType="circle" radialLines={false} stroke="rgba(148,163,184,.2)" />
              <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
              <RadialBar dataKey="value" cornerRadius={12} />
              <text x="50%" y="52%" textAnchor="middle" dominantBaseline="middle" fill="#c7f9ff" fontSize="28" fontWeight={700}>
                78%
              </text>
            </RadialBarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-12">
        <CardHeader>
          <CardTitle>Behavior Clustering Overview</CardTitle>
        </CardHeader>
        <CardContent className="h-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={behaviorClusters}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,.15)" />
              <XAxis dataKey="group" tick={{ fill: "#9ca3af", fontSize: 11 }} axisLine={false} tickLine={false} />
              <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={28} />
              <Tooltip />
              <Bar dataKey="z" fill="#00E5FF" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
}
