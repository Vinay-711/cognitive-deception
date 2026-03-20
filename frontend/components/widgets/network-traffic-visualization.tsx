"use client";

import { Area, AreaChart, CartesianGrid, Legend, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

export function NetworkTrafficVisualization() {
  const { metrics } = usePlatformMetrics();
  const base = metrics?.total_events || 0;
  
  const networkTrafficSeries = [
    { minute: "00", ingress: 320 + base, egress: 80 + base / 2 },
    { minute: "05", ingress: 540 + base, egress: 130 + base / 2 },
    { minute: "10", ingress: 680 + base * 2, egress: 190 + base / 2 },
    { minute: "15", ingress: 740 + base * 2, egress: 260 + base / 2 },
    { minute: "20", ingress: 630 + base, egress: 210 + base / 2 },
    { minute: "25", ingress: 710 + base, egress: 290 + base / 2 }
  ];

  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Network Traffic Visualization</CardTitle>
      </CardHeader>
      <CardContent className="h-[220px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={networkTrafficSeries}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.12)" />
            <XAxis dataKey="minute" tick={{ fill: "#9ca3af", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={28} />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="ingress" stroke="#00E5FF" fill="rgba(0,229,255,.2)" strokeWidth={2} />
            <Area type="monotone" dataKey="egress" stroke="#7C4DFF" fill="rgba(124,77,255,.2)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
