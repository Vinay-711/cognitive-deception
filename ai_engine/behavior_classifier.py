from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import math


@dataclass
class BehaviorPrediction:
    label: str
    confidence: float
    feature_vector: list[float]


class BehaviorClassifier:
    """Lightweight behavior classifier for demo and orchestration glue.

    This intentionally avoids heavyweight dependencies so it can run in all environments.
    """

    LABELS = ["script_kiddie", "automated_bot", "pentester", "apt_actor"]

    def featurize(self, command: str, typing_speed_cps: float, history: Sequence[str]) -> list[float]:
        cmd = command.lower()
        history_lower = [h.lower() for h in history]

        auto = sum(1 for k in ["masscan", "curl", "wget", "scan"] if k in cmd)
        exploit = sum(1 for k in ["sqlmap", "payload", "metasploit", "../", "' or"] if k in cmd)
        recon = sum(1 for k in ["nmap", "whois", "enum", "nikto"] if k in cmd)
        creds = sum(1 for k in ["hydra", "password", "sshpass", "brute"] if k in cmd)

        repeats = 0.0
        if history_lower:
            repeats = sum(1 for h in history_lower[-10:] if h == cmd) / float(min(10, len(history_lower)))

        token_count = len(cmd.split())
        entropy_like = 0.0
        if cmd:
            entropy_like = float(min(1.0, (math.sqrt(sum((ord(c) - 96) ** 2 for c in cmd)) / 400.0)))

        return [
            min(len(cmd) / 200.0, 1.0),
            min(token_count / 20.0, 1.0),
            min(typing_speed_cps / 12.0, 1.0),
            min(auto / 4.0, 1.0),
            min(exploit / 4.0, 1.0),
            min(recon / 4.0, 1.0),
            min(creds / 4.0, 1.0),
            repeats,
            entropy_like,
        ]

    def predict(self, command: str, typing_speed_cps: float, history: Sequence[str]) -> BehaviorPrediction:
        features = self.featurize(command, typing_speed_cps, history)
        cmd = command.lower()

        if any(k in cmd for k in ["proxychains", "cobalt", "powershell -enc"]):
            return BehaviorPrediction("apt_actor", 0.86, features)
        if any(k in cmd for k in ["sqlmap", "burp", "nikto", "nmap"]):
            return BehaviorPrediction("pentester", 0.78, features)
        if any(k in cmd for k in ["hydra", "password", "admin:admin"]):
            return BehaviorPrediction("script_kiddie", 0.74, features)
        if any(k in cmd for k in ["masscan", "wget", "curl -s", "bot"]):
            return BehaviorPrediction("automated_bot", 0.8, features)

        return BehaviorPrediction("script_kiddie", 0.62, features)
