import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { usePlatformMetrics } from "@/hooks/use-platform-metrics";

export function CognitiveBiasPanel() {
  const { metrics } = usePlatformMetrics();
  const cognitiveBiasScores = metrics?.cognitive_bias_scores || [];

  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Cognitive Bias Detection</CardTitle>
        <Badge variant="purple">Neuro-Symbolic</Badge>
      </CardHeader>
      <CardContent className="space-y-3">
        {cognitiveBiasScores.map((item) => (
          <div key={item.bias} className="space-y-1">
            <div className="flex items-center justify-between text-xs text-slate-300">
              <span>{item.bias}</span>
              <span>{item.score}%</span>
            </div>
            <div className="h-2 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full bg-gradient-to-r from-violet-500 to-cyan-400"
                style={{ width: `${item.score}%` }}
              />
            </div>
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
