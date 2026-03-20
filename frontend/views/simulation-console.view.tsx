"use client";

import { useMemo } from "react";

import { TerminalSimulator } from "@/components/widgets/terminal-simulator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useTerminalReplay } from "@/hooks/use-terminal-replay";

export function SimulationConsolePage() {
  const { commands } = useTerminalReplay();
  
  const timeline = useMemo(
    () => commands.map((command, index) => ({ at: `T+${index * 4}s`, command })),
    [commands]
  );

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-7">
        <TerminalSimulator title="Cyber Terminal – Live Attack Stream" />
      </div>

      <Card className="p-4 xl:col-span-5">
        <CardHeader>
          <CardTitle>AI Deception Response Log</CardTitle>
        </CardHeader>
        <CardContent className="max-h-[300px] space-y-3 overflow-y-auto">
          {timeline.map((item, index) => (
            <div key={item.at} className="rounded-lg border border-slate-700 bg-black/40 p-3">
              <p className="text-xs text-slate-500">{item.at}</p>
              <p className="mt-1 font-mono text-xs text-cyan-200">{item.command}</p>
              <p className="mt-1 text-xs text-violet-300">deception-ai: generated response profile #{410 + index}</p>
            </div>
          ))}
        </CardContent>
      </Card>

      <Card className="p-4 xl:col-span-12">
        <CardHeader>
          <CardTitle>Command Replay Timeline</CardTitle>
        </CardHeader>
        <CardContent className="overflow-x-auto">
          <div className="min-w-[760px] space-y-3">
            {timeline.map((item, index) => (
              <div key={item.at} className="flex items-center gap-3 text-sm">
                <span className="w-16 text-slate-400">{item.at}</span>
                <div className="h-2 w-2 rounded-full bg-cyan-400" />
                <div className="h-[1px] flex-1 bg-cyan-500/20" />
                <span className="w-[70%] font-mono text-cyan-200">{item.command}</span>
                <span className="text-xs text-slate-500">frame {index + 1}</span>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
