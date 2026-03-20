"use client";

import { CyberCard } from "@/components/ui/cyber-card";
import { NetworkGraph } from "@/components/visuals/network-graph";
import { useNetworkGraph } from "@/hooks/use-network-graph";

export default function NetworkTopologyPage() {
  const { graph } = useNetworkGraph();

  return (
    <div className="grid gap-5 xl:grid-cols-12">
      <div className="xl:col-span-8">
        <CyberCard title="Synthetic Infrastructure Topology">
          <NetworkGraph graph={graph} />
        </CyberCard>
      </div>

      <div className="xl:col-span-4 space-y-5">
        <CyberCard title="Key Nodes">
          <div className="space-y-3 text-sm text-slate-300">
            {graph.nodes.map((node) => (
              <div key={node.id} className="rounded-lg border border-slate-800 bg-black/40 p-3">
                <p className="text-cyan-200">{node.label}</p>
                <p className="text-xs text-slate-500">Group: {node.group}</p>
              </div>
            ))}
          </div>
        </CyberCard>

        <CyberCard title="Topology Insights">
          <p className="text-sm text-slate-300">
            Adaptive nodes are reweighted every 90 seconds to align with attacker reconnaissance paths.
          </p>
        </CyberCard>
      </div>
    </div>
  );
}
