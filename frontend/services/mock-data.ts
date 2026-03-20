const mockTimestampA = "2026-03-17T02:09:45.000Z";
const mockTimestampB = "2026-03-17T02:10:12.000Z";

export const mockAttackFeed = [
  {
    session_id: "sess-001",
    timestamp: mockTimestampA,
    source_ip: "203.0.113.10",
    command: "nmap -sV 10.10.44.0/24",
    attack_label: "reconnaissance",
    cognitive_bias: "overconfidence",
    deception_strategy: "surface_expansion",
    geo: { city: "Frankfurt", country: "DE", region: "EU" }
  },
  {
    session_id: "sess-002",
    timestamp: mockTimestampB,
    source_ip: "198.51.100.22",
    command: "hydra -l admin -P creds.txt ssh://10.10.44.7",
    attack_label: "credential_access",
    cognitive_bias: "confirmation_bias",
    deception_strategy: "credential_sinkhole",
    geo: { city: "Virginia", country: "US", region: "NA" }
  }
];

export const mockNetworkGraph = {
  nodes: [
    { id: "core", label: "Core Router", group: "core" },
    { id: "dmz", label: "DMZ Gateway", group: "dmz" },
    { id: "db", label: "Finance DB", group: "data" },
    { id: "hr", label: "HR Vault", group: "data" },
    { id: "emp-1", label: "Lena Brooks", group: "identity" }
  ],
  edges: [
    { source: "core", target: "dmz", label: "route" },
    { source: "core", target: "db", label: "route" },
    { source: "core", target: "hr", label: "route" }
  ]
};

export const mockDeceptionSessions = [
  {
    session_id: "sess-001",
    attacker_id: "GhostJackal",
    source_ip: "198.51.100.42",
    status: "active",
    deception_strategy: "baseline_obfuscation",
    cognitive_bias: "overconfidence",
    last_seen_at: mockTimestampA,
    synthetic_universe: {
      org_name: "Aether Dynamics",
      employees: [{ name: "Lena Brooks", role: "HR Manager" }]
    }
  }
];
