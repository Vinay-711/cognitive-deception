"use client";

import { motion } from "framer-motion";

import { AdversarialLearningProgress } from "@/components/widgets/adversarial-learning-progress";
import { CognitiveBiasPanel } from "@/components/widgets/cognitive-bias-panel";
import { DeceptionSuccessRate } from "@/components/widgets/deception-success-rate";
import { LiveActivityFeed } from "@/components/widgets/live-activity-feed";
import { MitreMappingGraph } from "@/components/widgets/mitre-mapping-graph";
import { NetworkTrafficVisualization } from "@/components/widgets/network-traffic-visualization";
import { TerminalSimulator } from "@/components/widgets/terminal-simulator";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useLiveThreatStream } from "@/hooks/use-live-threat-stream";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";
import { AttackHeatmapMap } from "@/visualizations/attack-heatmap-map";
import { ThreatGlobe } from "@/visualizations/threat-globe";

export function CommandCenterPage() {
  const { events, liveCount } = useLiveThreatStream();
  const { metrics, topAttackerType } = usePlatformMetrics();

  const metricCards = [
    { label: "Active Sessions", value: metrics?.active_sessions ?? liveCount + 18 },
    { label: "Observed Events", value: metrics?.total_events ?? 128 },
    { label: "Top Attacker Type", value: topAttackerType },
    { label: "Containment Delta", value: "+31%" }
  ];

  return (
    <div className="space-y-5">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {metricCards.map((metric) => (
          <motion.div key={metric.label} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
            <Card className="p-4">
              <p className="text-xs uppercase tracking-widest text-slate-400">{metric.label}</p>
              <p className="mt-2 text-2xl font-semibold text-cyan-100">{metric.value}</p>
            </Card>
          </motion.div>
        ))}
      </div>

      <div className="grid gap-5 xl:grid-cols-12">
        <Card className="p-4 xl:col-span-4">
          <CardHeader>
            <CardTitle>3D Global Attack Origin Globe</CardTitle>
          </CardHeader>
          <CardContent>
            <ThreatGlobe />
          </CardContent>
        </Card>

        <Card className="p-4 xl:col-span-8">
          <CardHeader>
            <CardTitle>Animated Attack Path Heatmap</CardTitle>
          </CardHeader>
          <CardContent>
            <AttackHeatmapMap />
          </CardContent>
        </Card>

        <div className="xl:col-span-4">
          <LiveActivityFeed events={events} />
        </div>

        <div className="space-y-5 xl:col-span-4">
          <CognitiveBiasPanel />
          <AdversarialLearningProgress />
        </div>

        <div className="space-y-5 xl:col-span-4">
          <MitreMappingGraph />
          <TerminalSimulator />
        </div>

        <div className="xl:col-span-6">
          <DeceptionSuccessRate />
        </div>

        <div className="xl:col-span-6">
          <NetworkTrafficVisualization />
        </div>
      </div>
    </div>
  );
}
