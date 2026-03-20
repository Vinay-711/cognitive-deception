from __future__ import annotations

from collections import Counter

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from cognitive_deception.demo.scenario_runner import demo_runner
from cognitive_deception.models.entities import AttackEvent, AttackSession, ThreatReport
from cognitive_deception.models.schemas import (
    AttackEventRecord,
    AttackFeedRecord,
    AnalysisSummary,
    CommandRequest,
    CommandResponse,
    DashboardMetrics,
    DeceptionSessionOverview,
    DemoScenarioResult,
    MitreHeatRecord,
    CognitiveBiasRecord,
    NetworkGraph,
    NetworkEdge,
    NetworkNode,
    SessionResponse,
    StartSessionRequest,
    ThreatReportResponse,
)
from cognitive_deception.models.db import get_db
from cognitive_deception.services.orchestrator import orchestrator

router = APIRouter()


@router.post("/sessions/start", response_model=SessionResponse)
def start_session(payload: StartSessionRequest, db: Session = Depends(get_db)) -> SessionResponse:
    session = orchestrator.start_session(
        db=db,
        attacker_id=payload.attacker_id,
        source_ip=payload.source_ip,
        channel=payload.channel,
    )

    synthetic_universe = session.metadata_json.get("synthetic_universe", {})
    return SessionResponse(
        session_id=session.id,
        attacker_id=session.attacker_id,
        source_ip=session.source_ip,
        channel=session.channel,
        attacker_type=session.attacker_type,
        cognitive_bias=session.cognitive_bias,
        deception_strategy=session.deception_strategy,
        synthetic_universe=synthetic_universe,
    )


@router.post("/sessions/{session_id}/command", response_model=CommandResponse)
def execute_command(session_id: str, payload: CommandRequest, db: Session = Depends(get_db)) -> CommandResponse:
    session = db.query(AttackSession).filter(AttackSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status != "active":
        raise HTTPException(status_code=409, detail="Session is not active")

    processed = orchestrator.process_command(
        db=db,
        session=session,
        command=payload.command,
        typing_duration_ms=payload.typing_duration_ms,
    )

    event = processed.event
    session = processed.session

    return CommandResponse(
        session_id=session.id,
        timestamp=event.timestamp,
        command=event.command,
        response=event.response,
        attack_label=event.attack_label,
        attack_confidence=event.attack_confidence,
        attacker_type=session.attacker_type,
        cognitive_bias=session.cognitive_bias,
        deception_strategy=session.deception_strategy,
        mitre_technique=event.mitre_technique,
        mitre_name=event.mitre_name,
        risk_score=event.risk_score,
    )


@router.get("/sessions/{session_id}/events", response_model=list[AttackEventRecord])
def get_session_events(session_id: str, db: Session = Depends(get_db)) -> list[AttackEventRecord]:
    session = db.query(AttackSession).filter(AttackSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    rows = db.query(AttackEvent).filter(AttackEvent.session_id == session_id).order_by(AttackEvent.timestamp.asc()).all()
    return [
        AttackEventRecord(
            id=row.id,
            session_id=row.session_id,
            timestamp=row.timestamp,
            command=row.command,
            response=row.response,
            attack_label=row.attack_label,
            attacker_type=session.attacker_type,
            cognitive_bias=row.cognitive_bias,
            deception_strategy=session.deception_strategy,
            mitre_technique=row.mitre_technique,
            mitre_name=row.mitre_name,
            risk_score=row.risk_score,
        )
        for row in rows
    ]


@router.get("/events/latest", response_model=list[AttackEventRecord])
def get_latest_events(limit: int = 50, db: Session = Depends(get_db)) -> list[AttackEventRecord]:
    rows = db.query(AttackEvent).order_by(AttackEvent.timestamp.desc()).limit(limit).all()
    # Return reversed to list them oldest to newest locally per slice, or newest first?
    # the frontend feed expects events where usually newest is at index 0 or pushed. Let's return as is.
    return [
        AttackEventRecord(
            id=row.id,
            session_id=row.session_id,
            timestamp=row.timestamp,
            command=row.command,
            response=row.response,
            attack_label=row.attack_label,
            attacker_type=row.session.attacker_type if row.session else "unknown",
            cognitive_bias=row.cognitive_bias,
            deception_strategy=row.session.deception_strategy if row.session else "baseline",
            mitre_technique=row.mitre_technique,
            mitre_name=row.mitre_name,
            risk_score=row.risk_score,
        )
        for row in rows
    ]


@router.get("/dashboard/metrics", response_model=DashboardMetrics)
def get_metrics(db: Session = Depends(get_db)) -> DashboardMetrics:
    sessions = db.query(AttackSession).all()
    events = db.query(AttackEvent).all()

    active_sessions = sum(1 for session in sessions if session.status == "active")
    attacker_type_counts = Counter(session.attacker_type for session in sessions)
    attack_label_counts = Counter(event.attack_label for event in events)
    bias_counts = Counter(event.cognitive_bias for event in events)
    strategy_counts = Counter(session.deception_strategy for session in sessions)

    mitre_counts = Counter(event.mitre_technique for event in events)
    mitre_heat = [MitreHeatRecord(technique=t, intensity=c * 15) for t, c in mitre_counts.items()]

    cognitive_bias_scores = [CognitiveBiasRecord(bias=b, score=c * 15) for b, c in bias_counts.items()]

    return DashboardMetrics(
        active_sessions=active_sessions,
        total_events=len(events),
        attacker_type_counts=dict(attacker_type_counts),
        attack_label_counts=dict(attack_label_counts),
        bias_counts=dict(bias_counts),
        strategy_counts=dict(strategy_counts),
        mitre_heat=mitre_heat,
        cognitive_bias_scores=cognitive_bias_scores,
    )


@router.post("/demo/run", response_model=DemoScenarioResult)
def run_demo(db: Session = Depends(get_db)) -> DemoScenarioResult:
    scenario_id, summary, steps = demo_runner.run(db=db)

    responses = []
    for processed in steps:
        event = processed.event
        session = processed.session
        responses.append(
            CommandResponse(
                session_id=session.id,
                timestamp=event.timestamp,
                command=event.command,
                response=event.response,
                attack_label=event.attack_label,
                attack_confidence=event.attack_confidence,
                attacker_type=session.attacker_type,
                cognitive_bias=session.cognitive_bias,
                deception_strategy=session.deception_strategy,
                mitre_technique=event.mitre_technique,
                mitre_name=event.mitre_name,
                risk_score=event.risk_score,
            )
        )

    return DemoScenarioResult(scenario_id=scenario_id, summary=summary, steps=responses)


@router.post("/reports/generate", response_model=ThreatReportResponse)
def generate_report(db: Session = Depends(get_db)) -> ThreatReportResponse:
    report = orchestrator.generate_report(db=db)
    return ThreatReportResponse(
        report_id=report.id,
        created_at=report.created_at,
        title=report.title,
        summary=report.summary,
        report_json=report.report_json,
    )


@router.get("/reports", response_model=list[ThreatReportResponse])
def list_reports(db: Session = Depends(get_db)) -> list[ThreatReportResponse]:
    reports = db.query(ThreatReport).order_by(ThreatReport.created_at.desc()).all()
    return [
        ThreatReportResponse(
            report_id=row.id,
            created_at=row.created_at,
            title=row.title,
            summary=row.summary,
            report_json=row.report_json,
        )
        for row in reports
    ]


@router.get("/deception", response_model=list[DeceptionSessionOverview])
def get_deception_overview(db: Session = Depends(get_db)) -> list[DeceptionSessionOverview]:
    sessions = (
        db.query(AttackSession)
        .order_by(AttackSession.last_seen_at.desc())
        .limit(40)
        .all()
    )
    return [
        DeceptionSessionOverview(
            session_id=session.id,
            attacker_id=session.attacker_id,
            source_ip=session.source_ip,
            status=session.status,
            deception_strategy=session.deception_strategy,
            cognitive_bias=session.cognitive_bias,
            last_seen_at=session.last_seen_at,
            synthetic_universe=session.metadata_json.get("synthetic_universe", {}),
        )
        for session in sessions
    ]


@router.get("/attacks", response_model=list[AttackFeedRecord])
def get_attack_feed(db: Session = Depends(get_db)) -> list[AttackFeedRecord]:
    events = db.query(AttackEvent).order_by(AttackEvent.timestamp.desc()).limit(120).all()
    feed: list[AttackFeedRecord] = []
    for event in events:
        session = event.session
        feed.append(
            AttackFeedRecord(
                session_id=event.session_id,
                timestamp=event.timestamp,
                source_ip=session.source_ip if session else "unknown",
                command=event.command,
                attack_label=event.attack_label,
                cognitive_bias=event.cognitive_bias,
                deception_strategy=session.deception_strategy if session else "baseline",
                geo=event.metadata_json.get("geo") if event.metadata_json else None,
            )
        )
    return feed


@router.get("/analysis", response_model=AnalysisSummary)
def get_analysis(db: Session = Depends(get_db)) -> AnalysisSummary:
    sessions = db.query(AttackSession).all()
    events = db.query(AttackEvent).all()
    attacker_type_counts = Counter(session.attacker_type for session in sessions)
    bias_counts = Counter(event.cognitive_bias for event in events)
    mitre_counts = Counter(event.mitre_technique for event in events)
    mitre_heat = [MitreHeatRecord(technique=t, intensity=c * 15) for t, c in mitre_counts.items()]

    top_attacker_type = attacker_type_counts.most_common(1)[0][0] if attacker_type_counts else "unknown"
    top_bias = bias_counts.most_common(1)[0][0] if bias_counts else "unknown"

    return AnalysisSummary(
        active_sessions=sum(1 for session in sessions if session.status == "active"),
        total_events=len(events),
        top_attacker_type=top_attacker_type,
        top_bias=top_bias,
        mitre_heat=mitre_heat,
    )


@router.get("/network", response_model=NetworkGraph)
def get_network_graph(db: Session = Depends(get_db)) -> NetworkGraph:
    session = db.query(AttackSession).order_by(AttackSession.last_seen_at.desc()).first()
    universe = session.metadata_json.get("synthetic_universe", {}) if session else {}

    nodes = [
        NetworkNode(id="core", label="Core Router", group="core"),
        NetworkNode(id="dmz", label="DMZ Gateway", group="dmz"),
        NetworkNode(id="db", label="Finance DB", group="data"),
        NetworkNode(id="hr", label="HR Vault", group="data"),
    ]

    for idx, employee in enumerate(universe.get("employees", [])[:6]):
        nodes.append(NetworkNode(id=f"emp-{idx}", label=employee.get("name", "Employee"), group="identity"))

    edges = [
        NetworkEdge(source="core", target="dmz", label="route"),
        NetworkEdge(source="core", target="db", label="route"),
        NetworkEdge(source="core", target="hr", label="route"),
    ]

    return NetworkGraph(nodes=nodes, edges=edges)

@router.websocket("/ws/telemetry")
async def telemetry_stream(websocket: WebSocket):
    await websocket.accept()
    queue = orchestrator.pipeline.subscribe()
    try:
        while True:
            event = await queue.get()
            await websocket.send_json(event)
    except WebSocketDisconnect:
        pass
    finally:
        orchestrator.pipeline.unsubscribe(queue)
