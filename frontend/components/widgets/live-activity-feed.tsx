"use client";

import { motion } from "framer-motion";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { type AttackEventRecord } from "@/services/api-client";
import { formatTimeUtc } from "@/lib/time";

const labelVariantMap: Record<string, "default" | "alert" | "purple"> = {
  reconnaissance: "default",
  brute_force: "alert",
  pattern_exploitation: "purple",
  data_exfiltration: "alert"
};

export function LiveActivityFeed({ events }: { events: AttackEventRecord[] }) {
  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Live Attacker Activity Feed</CardTitle>
        <Badge variant="default">Streaming</Badge>
      </CardHeader>
      <CardContent className="max-h-[320px] space-y-3 overflow-y-auto pr-1">
        {events.slice(0, 9).map((event, index) => (
          <motion.div
            key={event.id}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.25, delay: index * 0.02 }}
            className="rounded-xl border border-slate-700/70 bg-slate-950/40 p-3"
          >
            <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
              <span>{formatTimeUtc(event.timestamp)} UTC</span>
              <Badge variant={labelVariantMap[event.attack_label] || "default"}>{event.attack_label.replace("_", " ")}</Badge>
            </div>
            <p className="font-medium text-slate-100">{event.attacker_type} · Risk: {event.risk_score}</p>
            <p className="mt-1 font-mono text-xs text-cyan-200">{event.command}</p>
            <p className="mt-1 text-xs text-slate-500">Mitre: {event.mitre_technique} · {event.mitre_name}</p>
          </motion.div>
        ))}
      </CardContent>
    </Card>
  );
}
