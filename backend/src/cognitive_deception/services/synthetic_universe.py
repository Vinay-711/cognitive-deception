from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import Any


@dataclass
class SyntheticUniverse:
    org_name: str
    employees: list[dict[str, Any]]
    files: list[str]
    credentials: list[dict[str, str]]
    emails: list[dict[str, str]]
    chat_logs: list[dict[str, str]]


class SyntheticUniverseService:
    """Builds a fake corporate universe used as adaptive deception context."""

    def __init__(self) -> None:
        self.random = Random(17)
        self.first_names = ["Aisha", "Rohan", "Mina", "Lucas", "Elena", "Victor", "Nora", "Jamal", "Priya"]
        self.last_names = ["Singh", "Carter", "Ilyas", "Moreno", "Huang", "Bennett", "Rahman", "Patel"]
        self.roles = [
            "SOC Analyst",
            "Cloud Security Engineer",
            "Finance Operations Manager",
            "HR Systems Lead",
            "Platform Reliability Engineer",
            "Threat Intelligence Researcher",
            "Legal Compliance Officer",
        ]
        self.companies = ["Helix", "Northbridge", "Aether", "Sentinel", "Vector", "Axiom", "Orchid"]

    def _employee(self) -> dict[str, str]:
        first = self.random.choice(self.first_names)
        last = self.random.choice(self.last_names)
        username = f"{first.lower()}.{last.lower()}"
        company = self.random.choice(self.companies).lower()

        return {
            "name": f"{first} {last}",
            "role": self.random.choice(self.roles),
            "email": f"{username}@{company}.corp.local",
            "linkedin": f"https://www.linkedin.com/in/{username}",
        }

    def build(self, attacker_id: str) -> SyntheticUniverse:
        org_name = f"{self.random.choice(self.companies)} Holdings"
        employees = []
        for _ in range(8):
            employees.append(self._employee())

        files = [
            "/srv/hr/payroll_2026_q1.xlsx",
            "/srv/finance/vendor_wire_instructions.pdf",
            "/srv/engineering/roadmap_ai_defense.md",
            "/srv/legal/acquisition_draft_v5.docx",
            "/srv/ops/vpn_client_rollout_plan.txt",
        ]

        credentials = [
            {"principal": "svc_backup", "secret": "svc_backup@2026!"},
            {"principal": "db_replica", "secret": "ReplicaSync#902"},
            {"principal": "vpn-admin", "secret": "VpnTemp!447"},
        ]

        emails = [
            {
                "from": employees[0]["email"],
                "to": employees[1]["email"],
                "subject": "Updated finance consolidation pack",
            },
            {
                "from": employees[2]["email"],
                "to": employees[3]["email"],
                "subject": "SOC audit exceptions review",
            },
        ]

        chat_logs = [
            {
                "channel": "#finance-ops",
                "message": "Can someone rotate the legacy SFTP credentials before close of business?",
            },
            {
                "channel": "#it-admin",
                "message": f"{attacker_id} triggered unusual login alerts in SIEM overnight.",
            },
        ]

        return SyntheticUniverse(
            org_name=org_name,
            employees=employees,
            files=files,
            credentials=credentials,
            emails=emails,
            chat_logs=chat_logs,
        )
