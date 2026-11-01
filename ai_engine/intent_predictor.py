from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class IntentPrediction:
    intent: str
    confidence: float


class IntentPredictor:
    """Rule-first intent prediction for attacker commands."""

    def predict(self, command: str) -> IntentPrediction:
        cmd = command.lower()

        def has_indicator(indicators: list[str]) -> bool:
            return any(re.search(r"(?<!\w)" + re.escape(word) + r"(?!\w)", cmd)
                       for word in indicators)

        if has_indicator(["nmap", "scan", "whois", "dirb", "nikto"]):
            return IntentPrediction("reconnaissance", 0.82)
        if has_indicator(["hydra", "password", "sshpass", "brute"]):
            return IntentPrediction("credential_access", 0.85)
        if has_indicator(["sqlmap", "payload", "exploit", "metasploit"]):
            return IntentPrediction("exploit", 0.88)
        if has_indicator(["scp", "tar", "exfil", "dump"]):
            return IntentPrediction("exfiltration", 0.8)
        return IntentPrediction("low_signal", 0.55)
