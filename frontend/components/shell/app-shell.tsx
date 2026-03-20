"use client";

import { motion } from "framer-motion";
import { type ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { SidebarNavigation } from "@/components/nav/sidebar-navigation";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-cyber-bg text-slate-100">
      <div className="relative flex">
        <SidebarNavigation />

        <main className="w-full px-5 py-5 md:px-8 xl:px-10">
          <motion.header
            initial={{ opacity: 0, y: -12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.35 }}
            className="mb-6 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-cyan-500/20 bg-black/30 p-4 backdrop-blur-xl"
          >
            <div>
              <p className="text-xs uppercase tracking-[0.22em] text-slate-400">Adaptive Honeypot Intelligence</p>
              <h2 className="mt-1 text-lg font-semibold text-cyan-100">Cognitive Deception Operations Layer</h2>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="default">Live Telemetry</Badge>
              <Badge variant="purple">Neuro-Symbolic AI</Badge>
            </div>
          </motion.header>

          {children}
        </main>
      </div>
    </div>
  );
}
