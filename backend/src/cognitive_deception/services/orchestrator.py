from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import desc
from sqlalchemy.orm import Session

from cognitive_deception.ai.attack_strategy_simulator import AttackStrategySimulator
from cognitive_deception.ai.behavior_classifier import BehaviorClassifier
from cognitive_deception.ai.cognitive_bias_predictor import CognitiveBiasPredictor
from cognitive_deception.ai.llm_deception_generator import LLMDeceptionGenerator
from cognitive_deception.ai.threat_pattern_detector import ThreatPatternDetector
from cognitive_deception.core.config import get_settings
from cognitive_deception.knowledge.graph_engine import KnowledgeGraphEngine
from cognitive_deception.knowledge.mitre_mapper import MitreMapper
from cognitive_deception.models.entities import AttackEvent, AttackSession, ThreatReport
from cognitive_deception.services.deception_engine import DeceptionEngine
from cognitive_deception.services.geolocation import geolocate
from cognitive_deception.services.persona_engine import PersonaEngine
from cognitive_deception.services.synthetic_universe import SyntheticUniverseService
from cognitive_deception.streaming.pipeline import EventPipeline


@dataclass
class ProcessedEvent:
    event: AttackEvent
    session: AttackSession


class CognitiveDeceptionOrchestrator:
    def __init__(self) -> None:
        self.settings = get_settings()

        self.behavior = BehaviorClassifier()
        self.bias_predictor = CognitiveBiasPredictor()
        self.pattern_detector = ThreatPatternDetector()
        self.strategy_sim = AttackStrategySimulator()
        self.llm = LLMDeceptionGenerator()

        self.universe_service = SyntheticUniverseService()
        self.persona_engine = PersonaEngine()
        self.deception_engine = DeceptionEngine()

        self.mitre_mapper = MitreMapper()
        self.graph = KnowledgeGraphEngine()
        self.pipeline = EventPipeline()

        self.behavior.train()

    def start_session(self, db: Session, attacker_id: str, source_ip: str, channel: str) -> AttackSession:
        universe = self.universe_service.build(attacker_id=attacker_id)
        session = AttackSession(
            attacker_id=attacker_id,
            source_ip=source_ip,
            channel=channel,
            status="active",
            attacker_type="unknown",
            cognitive_bias="unknown",
            deception_strategy="baseline_obfuscation",
            metadata_json={
                "synthetic_universe": {
                    "org_name": universe.org_name,
                    "employees": universe.employees,
                    "files": universe.files,
                    "credentials": universe.credentials,
                    "emails": universe.emails,
                    "chat_logs": universe.chat_logs,
                }
            },
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def _typing_speed(self, command: str, typing_duration_ms: float) -> float:
        if typing_duration_ms <= 0:
            return max(1.0, len(command) / 4.0)
        return max(0.2, len(command) / max(typing_duration_ms / 1000.0, 0.1))

    def process_command(self, db: Session, session: AttackSession, command: str, typing_duration_ms: float) -> ProcessedEvent:
        command = command.strip()[: self.settings.max_command_length]

        history_rows = (
            db.query(AttackEvent)
            .filter(AttackEvent.session_id == session.id)
            .order_by(desc(AttackEvent.timestamp))
            .limit(self.settings.max_session_events)
            .all()
        )
        history = [row.command for row in reversed(history_rows)]
        repeats_ratio = 0.0
        if history:
            repeats_ratio = sum(1 for item in history[-8:] if item.lower() == command.lower()) / float(min(8, len(history)))

        typing_speed = self._typing_speed(command=command, typing_duration_ms=typing_duration_ms)

        classification = self.behavior.predict(command=command, typing_speed_cps=typing_speed, history=history)
        pattern = self.pattern_detector.detect(command=command, history=history)
        bias = self.bias_predictor.predict(
            command=command,
            typing_speed_cps=typing_speed,
            repeats_ratio=repeats_ratio,
            attack_label=classification.label,
        )
        strategy = self.strategy_sim.decide(
            attack_label=classification.label,
            bias=bias.bias,
            exploit_pattern=pattern.exploit_pattern,
            severity=pattern.severity,
        )
        mitre = self.mitre_mapper.map_pattern(pattern.exploit_pattern)

        universe = session.metadata_json.get("synthetic_universe", {})
        deception_profile = self.deception_engine.apply(strategy=strategy.strategy, universe=universe)

        # Social engineering simulation: attacker asking for employee/credential detail triggers persona response.
        if any(k in command.lower() for k in ["email", "employee", "hr", "linkedin", "who is"]):
            persona = universe.get("employees", [{"name": "Lena Brooks", "role": "HR Manager", "email": "hr@corp.local"}])[0]
            response = self.persona_engine.respond(persona=persona, prompt=command)
        else:
            response = self.llm.generate(
                channel=session.channel,
                command=command,
                strategy=strategy.strategy,
                deception_state=deception_profile.state,
                context={
                    "attacker_id": session.attacker_id,
                    "attacker_type": classification.label,
                    "bias": bias.bias,
                    "mitre": mitre.technique_id,
                },
            )

        event = AttackEvent(
            session_id=session.id,
            command=command,
            response=response,
            command_latency_ms=round(pattern.severity * 140.0, 3),
            typing_speed_cps=round(typing_speed, 4),
            tool_signature=pattern.tool_signature,
            exploit_pattern=pattern.exploit_pattern,
            attack_label=classification.label,
            attack_confidence=classification.confidence,
            cognitive_bias=bias.bias,
            mitre_technique=mitre.technique_id,
            mitre_name=mitre.technique_name,
            risk_score=strategy.risk_score,
            metadata_json={
                "bias_score": bias.score,
                "bias_rationale": bias.rationale,
                "strategy_rationale": strategy.rationale,
                "feature_vector": classification.feature_vector,
                "deception_state": deception_profile.state,
                "geo": geolocate(session.source_ip).__dict__,
            },
        )
        db.add(event)

        session.attacker_type = classification.label
        session.cognitive_bias = bias.bias
        session.deception_strategy = strategy.strategy
        session.last_seen_at = datetime.now(timezone.utc)
        session.metadata_json["latest_deception_state"] = deception_profile.state

        db.commit()
        db.refresh(event)
        db.refresh(session)

        event_record = {
            "event_id": event.id,
            "session_id": session.id,
            "timestamp": event.timestamp.isoformat(),
            "attacker_id": session.attacker_id,
            "source_ip": session.source_ip,
            "geo": geolocate(session.source_ip).__dict__,
            "command": event.command,
            "attack_label": event.attack_label,
            "tool_signature": event.tool_signature,
            "cognitive_bias": event.cognitive_bias,
            "mitre_technique": event.mitre_technique,
            "risk_score": event.risk_score,
            "strategy": session.deception_strategy,
        }
        self.pipeline.publish_event(event_record)
        self.graph.record_attack_edge(
            attacker=session.attacker_id,
            tool=event.tool_signature,
            technique=event.mitre_technique,
            target=session.channel,
            metadata={"risk_score": event.risk_score, "bias": event.cognitive_bias},
        )

        return ProcessedEvent(event=event, session=session)

    def generate_report(self, db: Session, title: str = "Threat Intelligence Report") -> ThreatReport:
        events = db.query(AttackEvent).order_by(desc(AttackEvent.timestamp)).limit(300).all()
        sessions = db.query(AttackSession).all()

        attack_label_counts = Counter(event.attack_label for event in events)
        bias_counts = Counter(event.cognitive_bias for event in events)
        strategy_counts = Counter(session.deception_strategy for session in sessions)

        summary = (
            f"Observed {len(events)} events across {len(sessions)} sessions. "
            f"Top attacker type: {attack_label_counts.most_common(1)[0][0] if attack_label_counts else 'none'}. "
            f"Top cognitive bias: {bias_counts.most_common(1)[0][0] if bias_counts else 'none'}."
        )

        report_json = {
            "kill_chain_progression": [
                {"phase": "Recon", "count": attack_label_counts.get("pentester", 0)},
                {"phase": "Credential Access", "count": sum(1 for e in events if e.exploit_pattern == "credential_attack")},
                {"phase": "Execution", "count": sum(1 for e in events if e.exploit_pattern == "exploit_injection")},
                {"phase": "Exfiltration", "count": sum(1 for e in events if e.exploit_pattern == "exfiltration")},
            ],
            "attacker_type_counts": dict(attack_label_counts),
            "cognitive_bias_counts": dict(bias_counts),
            "deception_strategy_counts": dict(strategy_counts),
            "knowledge_graph_edges": self.graph.get_local_snapshot(),
            "pipeline_preview": self.pipeline.latest(limit=20),
        }

        report = ThreatReport(title=title, summary=summary, report_json=report_json)
        db.add(report)
        db.commit()
        db.refresh(report)
        return report


orchestrator = CognitiveDeceptionOrchestrator()
