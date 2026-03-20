"use client";

import { useAttackFeed } from "@/hooks/use-attack-feed";
import { CyberCard } from "@/components/ui/cyber-card";
import { formatTimeUtc } from "@/lib/time";

export default function AttackConsolePage() {
  const { events } = useAttackFeed();

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-8">
        <CyberCard title="Interactive Attack Console" className="h-full">
          <div className="h-[520px] overflow-y-auto rounded-xl border border-slate-800 bg-black/70 p-4 font-mono text-xs text-cyan-200">
            {events.map((event, index) => (
              <div key={`${event.session_id}-${index}`} className="mb-3">
                <p className="text-slate-500">[{formatTimeUtc(event.timestamp)} UTC] {event.source_ip}</p>
                <p className="text-cyan-200">$ {event.command}</p>
                <p className="text-slate-400">response: deception engaged</p>
              </div>
            ))}
          </div>
        </CyberCard>
      </div>

      <div className="xl:col-span-4 space-y-5">
        <CyberCard title="Session Replay">
          <div className="space-y-3 text-sm text-slate-300">
            {events.slice(0, 5).map((event, idx) => (
              <div key={`${event.session_id}-replay-${idx}`} className="rounded-lg border border-slate-800 bg-black/40 p-3">
                <p className="text-cyan-200">{event.attack_label}</p>
                <p className="text-xs text-slate-500">{event.cognitive_bias}</p>
              </div>
            ))}
          </div>
        </CyberCard>

        <CyberCard title="AI Deception Responses">
          <div className="space-y-2 text-xs text-slate-400">
            <p>Adaptive response: deepened filesystem lure.</p>
            <p>Injected synthetic employee vault for social engineering bait.</p>
            <p>Updated service banners to mirror attacker toolchain expectations.</p>
          </div>
        </CyberCard>
      </div>
    </div>
  );
}
