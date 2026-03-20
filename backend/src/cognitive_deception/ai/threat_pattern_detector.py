from dataclasses import dataclass
from typing import Sequence


@dataclass
class ThreatPattern:
    exploit_pattern: str
    tool_signature: str
    severity: float


class ThreatPatternDetector:
    def detect(self, command: str, history: Sequence[str]) -> ThreatPattern:
        cmd = command.lower()
        history_lower = [h.lower() for h in history]

        if any(k in cmd for k in ["sqlmap", "' or", "../", "payload", "metasploit"]):
            return ThreatPattern("exploit_injection", "exploit_tooling", 0.9)

        if any(k in cmd for k in ["hydra", "password", "brute", "sshpass"]):
            return ThreatPattern("credential_attack", "credential_tooling", 0.82)

        if any(k in cmd for k in ["scp", "tar", "base64", "exfil", "dump"]):
            return ThreatPattern("exfiltration", "data_mover", 0.86)

        if sum(1 for item in history_lower[-8:] if "nmap" in item or "scan" in item) >= 3:
            return ThreatPattern("repetitive_scanning", "recon_suite", 0.74)

        if any(k in cmd for k in ["nmap", "enum", "whois", "dirb", "nikto"]):
            return ThreatPattern("reconnaissance", "recon_suite", 0.68)

        return ThreatPattern("low_signal", "generic_shell", 0.45)
