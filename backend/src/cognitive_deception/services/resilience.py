from __future__ import annotations

import asyncio
from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from cognitive_deception.core.config import get_settings
from cognitive_deception.models.db import SessionLocal
from cognitive_deception.models.entities import AttackSession


@dataclass
class ResilienceStats:
    expired_sessions: int


class ResilienceSupervisor:
    """Basic self-healing loop.

    - Expires idle sessions to avoid unbounded growth.
    - Designed to be extended with retraining and pipeline rechecks.
    """

    def __init__(self) -> None:
        settings = get_settings()
        self._interval = settings.resilience_interval_seconds
        self._idle_timeout = settings.session_idle_timeout_seconds
        self._running = False

    def expire_idle_sessions(self, db: Session) -> ResilienceStats:
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=self._idle_timeout)
        stale = (
            db.query(AttackSession)
            .filter(AttackSession.status == "active")
            .filter(AttackSession.last_seen_at < cutoff)
            .all()
        )
        for session in stale:
            session.status = "inactive"
        if stale:
            db.commit()
        return ResilienceStats(expired_sessions=len(stale))

    async def run(self) -> None:
        self._running = True
        while self._running:
            try:
                with SessionLocal() as db:
                    self.expire_idle_sessions(db)
            except Exception:
                # Avoid crashing the API loop on transient DB failures.
                pass
            await asyncio.sleep(self._interval)

    async def shutdown(self) -> None:
        self._running = False
        await asyncio.sleep(0)


async def run_resilience_loop() -> asyncio.Task:
    supervisor = ResilienceSupervisor()
    task = asyncio.create_task(supervisor.run())
    return task


async def shutdown_resilience_loop(task: asyncio.Task) -> None:
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
