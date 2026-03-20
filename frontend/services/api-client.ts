const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1";

export type MitreHeatRecord = {
  technique: string;
  intensity: number;
};

export type CognitiveBiasRecord = {
  bias: string;
  score: number;
};

export type AttackEventRecord = {
  id: number;
  session_id: string;
  timestamp: string;
  command: string;
  response: string;
  attack_label: string;
  attacker_type: string;
  cognitive_bias: string;
  deception_strategy: string;
  mitre_technique: string;
  mitre_name: string;
  risk_score: number;
};

export type AttackFeedRecord = {
  session_id: string;
  timestamp: string;
  source_ip: string;
  command: string;
  attack_label: string;
  cognitive_bias: string;
  deception_strategy: string;
  geo?: { city: string; country: string; region: string } | null;
};

export type DeceptionSessionOverview = {
  session_id: string;
  attacker_id: string;
  source_ip: string;
  status: string;
  deception_strategy: string;
  cognitive_bias: string;
  last_seen_at: string;
  synthetic_universe: Record<string, unknown>;
};

export type AnalysisSummary = {
  active_sessions: number;
  total_events: number;
  top_attacker_type: string;
  top_bias: string;
  mitre_heat: MitreHeatRecord[];
};

export type NetworkNode = { id: string; label: string; group: string };
export type NetworkEdge = { source: string; target: string; label: string };
export type NetworkGraph = { nodes: NetworkNode[]; edges: NetworkEdge[] };

export type PlatformMetrics = {
  active_sessions: number;
  total_events: number;
  attacker_type_counts: Record<string, number>;
  attack_label_counts: Record<string, number>;
  bias_counts: Record<string, number>;
  strategy_counts: Record<string, number>;
  mitre_heat: MitreHeatRecord[];
  cognitive_bias_scores: CognitiveBiasRecord[];
};

export async function fetchPlatformMetrics(): Promise<PlatformMetrics> {
  const response = await fetch(`${API_BASE}/dashboard/metrics`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`metrics fetch failed: ${response.status}`);
  }

  return (await response.json()) as PlatformMetrics;
}

export async function fetchLatestEvents(): Promise<AttackEventRecord[]> {
  const response = await fetch(`${API_BASE}/events/latest`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    cache: "no-store"
  });

  if (!response.ok) {
    throw new Error(`events fetch failed: ${response.status}`);
  }

  return (await response.json()) as AttackEventRecord[];
}

export async function fetchDeceptionSessions(): Promise<DeceptionSessionOverview[]> {
  const response = await fetch(`${API_BASE}/deception`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`deception fetch failed: ${response.status}`);
  }
  return (await response.json()) as DeceptionSessionOverview[];
}

export async function fetchAttacks(): Promise<AttackFeedRecord[]> {
  const response = await fetch(`${API_BASE}/attacks`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`attacks fetch failed: ${response.status}`);
  }
  return (await response.json()) as AttackFeedRecord[];
}

export async function fetchAnalysis(): Promise<AnalysisSummary> {
  const response = await fetch(`${API_BASE}/analysis`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`analysis fetch failed: ${response.status}`);
  }
  return (await response.json()) as AnalysisSummary;
}

export async function fetchNetworkGraph(): Promise<NetworkGraph> {
  const response = await fetch(`${API_BASE}/network`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`network fetch failed: ${response.status}`);
  }
  return (await response.json()) as NetworkGraph;
}
