"use client";

import { useMemo } from "react";

import { type NetworkGraph } from "@/services/api-client";

export function NetworkGraph({ graph }: { graph: NetworkGraph }) {
  const nodes = useMemo(() => graph.nodes, [graph.nodes]);
  const edges = useMemo(() => graph.edges, [graph.edges]);

  return (
    <div className="relative h-[280px] rounded-2xl border border-cyan-500/20 bg-[radial-gradient(circle_at_20%_20%,rgba(0,229,255,.12),transparent_45%),radial-gradient(circle_at_80%_80%,rgba(124,77,255,.12),transparent_40%),#05070a]">
      <svg viewBox="0 0 600 320" className="h-full w-full">
        {edges.map((edge, idx) => {
          const source = nodes.find((n) => n.id === edge.source) ?? nodes[0];
          const target = nodes.find((n) => n.id === edge.target) ?? nodes[0];
          const sx = 120 + nodes.indexOf(source) * 80;
          const sy = 80 + (nodes.indexOf(source) % 2) * 120;
          const tx = 120 + nodes.indexOf(target) * 80;
          const ty = 80 + (nodes.indexOf(target) % 2) * 120;
          return (
            <line
              key={`edge-${idx}`}
              x1={sx}
              y1={sy}
              x2={tx}
              y2={ty}
              stroke="rgba(0,229,255,0.25)"
              strokeWidth={2}
            />
          );
        })}
        {nodes.map((node, idx) => {
          const x = 120 + idx * 80;
          const y = 80 + (idx % 2) * 120;
          return (
            <g key={node.id}>
              <circle cx={x} cy={y} r={16} fill="rgba(0,229,255,0.35)" />
              <circle cx={x} cy={y} r={8} fill="#00E5FF" />
              <text x={x} y={y + 30} textAnchor="middle" fill="#9BDFF1" fontSize="10">
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
