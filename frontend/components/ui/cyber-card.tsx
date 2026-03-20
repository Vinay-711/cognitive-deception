import { ReactNode } from "react";

import { cn } from "@/lib/utils";

export function CyberCard({ title, children, className }: { title: string; children: ReactNode; className?: string }) {
  return (
    <section
      className={cn(
        "rounded-2xl border border-cyan-500/15 bg-cyber-panel/70 p-4 shadow-neon backdrop-blur-xl",
        className
      )}
    >
      <header className="mb-4 flex items-center justify-between">
        <h3 className="text-sm font-semibold tracking-wide text-cyan-100">{title}</h3>
      </header>
      {children}
    </section>
  );
}
