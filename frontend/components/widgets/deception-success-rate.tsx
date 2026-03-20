"use client";

import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

export function DeceptionSuccessRate() {
  const { metrics } = usePlatformMetrics();
  const base = Math.min((metrics?.active_sessions || 0) * 2, 100);

  const successRateSeries = [
    { t: "00:00", rate: Math.max(0, 61 - base) },
    { t: "00:05", rate: Math.max(0, 67 - base) },
    { t: "00:10", rate: 73 },
    { t: "00:15", rate: 76 },
    { t: "00:20", rate: Math.min(100, 81 + base) },
    { t: "00:25", rate: Math.min(100, 84 + base) }
  ];

  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Real-Time Deception Success Rate</CardTitle>
        <Badge variant="default">{Math.min(100, 84 + base)}%</Badge>
      </CardHeader>
      <CardContent className="h-[210px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={successRateSeries}>
            <defs>
              <linearGradient id="successGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#00E5FF" stopOpacity={0.8} />
                <stop offset="95%" stopColor="#00E5FF" stopOpacity={0.05} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.12)" />
            <XAxis dataKey="t" tick={{ fill: "#9ca3af", fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: "#6b7280", fontSize: 11 }} axisLine={false} tickLine={false} width={28} />
            <Tooltip />
            <Area type="monotone" dataKey="rate" stroke="#00E5FF" fill="url(#successGradient)" strokeWidth={2} />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
