from datetime import datetime, timedelta, timezone

from cognitive_deception.models.db import SessionLocal
from cognitive_deception.models.entities import AttackSession
from cognitive_deception.services.resilience import ResilienceSupervisor


def test_expire_idle_sessions():
    supervisor = ResilienceSupervisor()
    with SessionLocal() as db:
        old_session = AttackSession(
            attacker_id="idle",
            source_ip="203.0.113.2",
            channel="ssh",
            status="active",
            last_seen_at=datetime.now(timezone.utc) - timedelta(hours=5),
        )
        db.add(old_session)
        db.commit()

        stats = supervisor.expire_idle_sessions(db)
        assert stats.expired_sessions >= 1

        refreshed = db.query(AttackSession).filter(AttackSession.id == old_session.id).first()
        assert refreshed.status == "inactive"
