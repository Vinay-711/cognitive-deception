"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

const navigationItems = [
  { href: "/", label: "Threat Command Center" },
  { href: "/attacker-profile", label: "Attacker Profile" },
  { href: "/deception-generator", label: "Deception Generator" },
  { href: "/simulation-console", label: "Attack Console" },
  { href: "/report-center", label: "Report Center" }
];

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <aside className="sticky top-0 hidden h-screen w-72 shrink-0 border-r border-cyan-500/20 bg-black/30 p-5 backdrop-blur-xl xl:block">
      <div className="mb-8 rounded-2xl border border-cyan-500/20 bg-cyan-500/5 p-4">
        <p className="text-xs uppercase tracking-[0.25em] text-cyan-200/70">Cognitive Deception</p>
        <h1 className="mt-2 text-xl font-semibold text-cyan-50">Neuro-Symbolic SOC</h1>
      </div>

      <nav className="space-y-2">
        {navigationItems.map((item) => {
          const active = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "flex rounded-xl px-3 py-2 text-sm transition-all",
                active
                  ? "border border-cyan-400/30 bg-cyan-400/20 text-cyan-100"
                  : "border border-transparent text-slate-300 hover:border-cyan-500/20 hover:bg-cyan-500/5"
              )}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
