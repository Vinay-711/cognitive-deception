from __future__ import annotations

from dataclasses import dataclass


MITRE_MAP = {
    "reconnaissance": ("T1595", "Active Scanning"),
    "credential_access": ("T1110", "Brute Force"),
    "exploit": ("T1190", "Exploit Public-Facing Application"),
    "exfiltration": ("T1041", "Exfiltration Over C2 Channel"),
}


@dataclass
class AttackPattern:
    pattern: str
    mitre_technique: str
    mitre_name: str
    severity: float


class AttackPatternClassifier:
    def classify(self, command: str) -> AttackPattern:
        cmd = command.lower()
        if any(k in cmd for k in ["nmap", "scan", "dirb"]):
            tech, name = MITRE_MAP["reconnaissance"]
            return AttackPattern("reconnaissance", tech, name, 0.6)
        if any(k in cmd for k in ["hydra", "password", "sshpass"]):
            tech, name = MITRE_MAP["credential_access"]
            return AttackPattern("credential_access", tech, name, 0.8)
        if any(k in cmd for k in ["sqlmap", "payload", "exploit"]):
            tech, name = MITRE_MAP["exploit"]
            return AttackPattern("exploit", tech, name, 0.9)
        if any(k in cmd for k in ["scp", "tar", "exfil"]):
            tech, name = MITRE_MAP["exfiltration"]
            return AttackPattern("exfiltration", tech, name, 0.85)
        return AttackPattern("low_signal", "T1059", "Command and Scripting Interpreter", 0.4)
