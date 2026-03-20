from __future__ import annotations

from dataclasses import dataclass


@dataclass
class IntentPrediction:
    intent: str
    confidence: float


class IntentPredictor:
    """Rule-first intent prediction for attacker commands."""

    def predict(self, command: str) -> IntentPrediction:
        cmd = command.lower()
        if any(k in cmd for k in ["nmap", "scan", "whois", "dirb", "nikto"]):
            return IntentPrediction("reconnaissance", 0.82)
        if any(k in cmd for k in ["hydra", "password", "sshpass", "brute"]):
            return IntentPrediction("credential_access", 0.85)
        if any(k in cmd for k in ["sqlmap", "payload", "exploit", "metasploit"]):
            return IntentPrediction("exploit", 0.88)
        if any(k in cmd for k in ["scp", "tar", "exfil", "dump"]):
            return IntentPrediction("exfiltration", 0.8)
        return IntentPrediction("low_signal", 0.55)
