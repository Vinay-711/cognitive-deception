"use client";

import { type AttackFeedRecord } from "@/services/api-client";
import { formatTimeUtc } from "@/lib/time";

export function AttackTimeline({ events }: { events: AttackFeedRecord[] }) {
  return (
    <div className="space-y-3">
      {events.slice(0, 6).map((event) => (
        <div key={`${event.session_id}-${event.timestamp}`} className="rounded-xl border border-slate-700/70 bg-slate-950/40 p-3">
          <div className="mb-1 flex items-center justify-between text-xs text-slate-400">
            <span>{formatTimeUtc(event.timestamp)} UTC</span>
            <span className="uppercase tracking-widest text-cyan-200">{event.attack_label}</span>
          </div>
          <p className="font-medium text-slate-100">{event.source_ip}</p>
          <p className="mt-1 font-mono text-xs text-cyan-200">{event.command}</p>
          <p className="mt-1 text-xs text-slate-500">
            Bias: {event.cognitive_bias} · Strategy: {event.deception_strategy}
          </p>
        </div>
      ))}
    </div>
  );
}
