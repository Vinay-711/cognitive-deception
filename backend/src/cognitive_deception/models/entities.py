from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from cognitive_deception.models.db import Base


class AttackSession(Base):
    __tablename__ = "attack_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    attacker_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    source_ip: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    channel: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(16), default="active", index=True)
    attacker_type: Mapped[str] = mapped_column(String(64), default="unknown", nullable=False)
    cognitive_bias: Mapped[str] = mapped_column(String(64), default="unknown", nullable=False)
    deception_strategy: Mapped[str] = mapped_column(String(64), default="baseline", nullable=False)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    events: Mapped[list["AttackEvent"]] = relationship("AttackEvent", back_populates="session", cascade="all, delete-orphan")


class AttackEvent(Base):
    __tablename__ = "attack_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("attack_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    command: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)
    command_latency_ms: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    typing_speed_cps: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    tool_signature: Mapped[str] = mapped_column(String(64), nullable=False)
    exploit_pattern: Mapped[str] = mapped_column(String(64), nullable=False)
    attack_label: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    attack_confidence: Mapped[float] = mapped_column(Float, nullable=False)
    cognitive_bias: Mapped[str] = mapped_column(String(64), nullable=False)

    mitre_technique: Mapped[str] = mapped_column(String(32), nullable=False)
    mitre_name: Mapped[str] = mapped_column(String(128), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)

    metadata_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)

    session: Mapped[AttackSession] = relationship("AttackSession", back_populates="events")


class ThreatReport(Base):
    __tablename__ = "threat_reports"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    title: Mapped[str] = mapped_column(String(128), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    report_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict, nullable=False)
