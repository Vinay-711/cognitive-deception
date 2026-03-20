from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StartSessionRequest(BaseModel):
    attacker_id: str
    source_ip: str
    channel: str = Field(pattern="^(ssh|http|api|dionaea|cowrie|honeypot|tcp)$")


class SessionResponse(BaseModel):
    session_id: str
    attacker_id: str
    source_ip: str
    channel: str
    attacker_type: str
    cognitive_bias: str
    deception_strategy: str
    synthetic_universe: dict[str, Any]


class CommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=2048)
    typing_duration_ms: float = 0.0


class CommandResponse(BaseModel):
    session_id: str
    timestamp: datetime
    command: str
    response: str
    attack_label: str
    attack_confidence: float
    attacker_type: str
    cognitive_bias: str
    deception_strategy: str
    mitre_technique: str
    mitre_name: str
    risk_score: float


class MitreHeatRecord(BaseModel):
    technique: str
    intensity: int


class CognitiveBiasRecord(BaseModel):
    bias: str
    score: int


class DashboardMetrics(BaseModel):
    active_sessions: int
    total_events: int
    attacker_type_counts: dict[str, int]
    attack_label_counts: dict[str, int]
    bias_counts: dict[str, int]
    strategy_counts: dict[str, int]
    mitre_heat: list[MitreHeatRecord]
    cognitive_bias_scores: list[CognitiveBiasRecord]


class DeceptionSessionOverview(BaseModel):
    session_id: str
    attacker_id: str
    source_ip: str
    status: str
    deception_strategy: str
    cognitive_bias: str
    last_seen_at: datetime
    synthetic_universe: dict[str, Any]


class AttackFeedRecord(BaseModel):
    session_id: str
    timestamp: datetime
    source_ip: str
    command: str
    attack_label: str
    cognitive_bias: str
    deception_strategy: str
    geo: dict[str, Any] | None = None


class AnalysisSummary(BaseModel):
    active_sessions: int
    total_events: int
    top_attacker_type: str
    top_bias: str
    mitre_heat: list[MitreHeatRecord]


class NetworkNode(BaseModel):
    id: str
    label: str
    group: str


class NetworkEdge(BaseModel):
    source: str
    target: str
    label: str


class NetworkGraph(BaseModel):
    nodes: list[NetworkNode]
    edges: list[NetworkEdge]


class DemoScenarioResult(BaseModel):
    scenario_id: str
    summary: str
    steps: list[CommandResponse]


class ThreatReportResponse(BaseModel):
    report_id: str
    created_at: datetime
    title: str
    summary: str
    report_json: dict[str, Any]


class AttackEventRecord(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_id: str
    timestamp: datetime
    command: str
    response: str
    attack_label: str
    attacker_type: str
    cognitive_bias: str
    deception_strategy: str
    mitre_technique: str
    mitre_name: str
    risk_score: float
