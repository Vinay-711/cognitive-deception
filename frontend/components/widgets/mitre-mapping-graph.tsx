"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

export function MitreMappingGraph() {
  const { metrics } = usePlatformMetrics();
  const mitreHeat = metrics?.mitre_heat || [];

  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>MITRE ATT&CK Mapping Graph</CardTitle>
      </CardHeader>
      <CardContent className="h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={mitreHeat}>
            <XAxis dataKey="technique" tick={{ fill: "#9ca3af", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={28} />
            <Tooltip cursor={{ fill: "rgba(0,229,255,0.08)" }} />
            <Bar dataKey="intensity" fill="#00E5FF" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
