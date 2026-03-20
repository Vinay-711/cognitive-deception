"use client";

import { useMemo } from "react";

export type GeoPoint = [number, number];
export type AttackArc = {
  source: GeoPoint;
  target: GeoPoint;
  weight: number;
};
const attackArcs: AttackArc[] = [
  { source: [-74.006, 40.7128], target: [77.209, 28.6139], weight: 62 },
  { source: [13.405, 52.52], target: [-0.1278, 51.5074], weight: 74 },
  { source: [103.8198, 1.3521], target: [139.6917, 35.6895], weight: 54 },
  { source: [37.6173, 55.7558], target: [151.2093, -33.8688], weight: 39 }
];

type Point = { x: number; y: number };

type ArcPath = {
  id: string;
  source: Point;
  target: Point;
  path: string;
  weight: number;
};

function project(lon: number, lat: number, width: number, height: number): Point {
  // Equirectangular projection for a lightweight, dependency-free global map.
  const x = ((lon + 180) / 360) * width;
  const y = ((90 - lat) / 180) * height;
  return { x, y };
}

export function AttackHeatmapMap() {
  const width = 980;
  const height = 380;

  const arcPaths = useMemo<ArcPath[]>(() => {
    return attackArcs.map((arc, idx) => {
      const source = project(arc.source[0], arc.source[1], width, height);
      const target = project(arc.target[0], arc.target[1], width, height);

      const midX = (source.x + target.x) / 2;
      const midY = (source.y + target.y) / 2 - Math.max(20, Math.abs(source.x - target.x) * 0.14);
      const path = `M ${source.x} ${source.y} Q ${midX} ${midY} ${target.x} ${target.y}`;

      return {
        id: `arc-${idx}`,
        source,
        target,
        path,
        weight: arc.weight
      };
    });
  }, [height, width]);

  return (
    <div className="relative h-[320px] overflow-hidden rounded-2xl border border-cyan-500/20 bg-[radial-gradient(circle_at_20%_20%,rgba(0,229,255,.18),transparent_35%),radial-gradient(circle_at_80%_60%,rgba(124,77,255,.18),transparent_40%),#06090f]">
      <svg viewBox={`0 0 ${width} ${height}`} className="h-full w-full">
        <defs>
          <linearGradient id="attackArcGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#7C4DFF" stopOpacity="0.65" />
            <stop offset="100%" stopColor="#FF3B3B" stopOpacity="0.88" />
          </linearGradient>
          <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
            <path d="M 28 0 L 0 0 0 28" fill="none" stroke="rgba(0,229,255,0.07)" strokeWidth="1" />
          </pattern>
          <filter id="glow">
            <feGaussianBlur stdDeviation="2.2" result="coloredBlur" />
            <feMerge>
              <feMergeNode in="coloredBlur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <rect x="0" y="0" width={width} height={height} fill="url(#grid)" />

        {arcPaths.map((arc) => (
          <g key={arc.id}>
            <path
              d={arc.path}
              fill="none"
              stroke="url(#attackArcGradient)"
              strokeWidth={Math.max(1.2, arc.weight / 24)}
              strokeLinecap="round"
              opacity={0.78}
              filter="url(#glow)"
              strokeDasharray="7 5"
            >
              <animate attributeName="stroke-dashoffset" from="0" to="-180" dur="3.8s" repeatCount="indefinite" />
            </path>
            <circle cx={arc.target.x} cy={arc.target.y} r={Math.max(2, arc.weight / 16)} fill="rgba(0,229,255,0.82)">
              <animate attributeName="r" values="2;5;2" dur="2.4s" repeatCount="indefinite" />
            </circle>
          </g>
        ))}
      </svg>

      <div className="pointer-events-none absolute bottom-3 left-3 rounded-lg border border-cyan-500/30 bg-black/40 px-3 py-1 text-xs text-cyan-100">
        Animated threat routes rendered in resilient fallback mode.
      </div>
    </div>
  );
}
