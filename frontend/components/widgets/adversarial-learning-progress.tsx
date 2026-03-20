import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";

const deceptionProgress = [
  { stage: "Entropy Injected", value: 62 },
  { stage: "Cognitive Drift", value: 74 },
  { stage: "TTP Diversion", value: 88 },
  { stage: "Payload Containment", value: 79 }
];

export function AdversarialLearningProgress() {
  return (
    <Card className="p-4">
      <CardHeader>
        <CardTitle>Adversarial Learning Progress</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {deceptionProgress.map((step) => (
          <div key={step.stage}>
            <div className="mb-1 flex items-center justify-between text-xs text-slate-300">
              <span>{step.stage}</span>
              <span>{step.value}%</span>
            </div>
            <Progress value={step.value} />
          </div>
        ))}
      </CardContent>
    </Card>
  );
}
