"use client";

import { motion } from "framer-motion";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useTerminalReplay } from "@/hooks/use-terminal-replay";

export function TerminalSimulator({ title = "Real-Time Terminal Simulation" }: { title?: string }) {
  const { commands, cursor } = useTerminalReplay();

  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        <Badge variant="alert">Honeypot stream</Badge>
      </CardHeader>
      <CardContent className="h-[230px] overflow-hidden rounded-xl border border-cyan-500/20 bg-black/70 p-4 font-mono text-xs text-cyan-300">
        {commands.map((command, index) => (
          <motion.p
            key={`${command}-${index}`}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-2"
          >
            <span className="text-cyan-500">root@decoy</span>:~$ {command}
          </motion.p>
        ))}
        <p className="text-violet-300">response: deceptive sandbox output id #{cursor + 201}</p>
      </CardContent>
    </Card>
  );
}
