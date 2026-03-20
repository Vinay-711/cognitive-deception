from __future__ import annotations

import importlib
from dataclasses import dataclass
from typing import Any, Sequence

import numpy as np

torch: Any | None = None
nn: Any | None = None
optim: Any | None = None

try:
    torch = importlib.import_module("torch")
    nn = importlib.import_module("torch.nn")
    optim = importlib.import_module("torch.optim")
except Exception:  # pragma: no cover
    torch = None
    nn = None
    optim = None


ATTACK_LABELS = ["script_kiddie", "automated_bot", "pentester", "apt_actor"]


@dataclass
class AttackClassification:
    label: str
    confidence: float
    feature_vector: list[float]


_NetBase: Any = nn.Module if nn is not None else object


class _Net(_NetBase):
    def __init__(self, input_dim: int, output_dim: int):
        if nn is None:
            raise RuntimeError("torch is not available")

        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 12),
            nn.ReLU(),
            nn.Linear(12, output_dim),
        )

    def forward(self, x: Any) -> Any:
        return self.layers(x)


class BehaviorClassifier:
    def __init__(self) -> None:
        self.input_dim = 10
        self.is_trained = False
        self.model = _Net(self.input_dim, len(ATTACK_LABELS)) if (torch is not None and nn is not None and optim is not None) else None

    def _features(self, command: str, typing_speed_cps: float, history: Sequence[str]) -> list[float]:
        cmd = command.lower()
        history_lower = [item.lower() for item in history]

        auto_signals = sum(1 for k in ["masscan", "curl", "wget", "bot", "scan"] if k in cmd)
        exploit_signals = sum(1 for k in ["sqlmap", "metasploit", "payload", "../", "' or"] if k in cmd)
        opsec_signals = sum(1 for k in ["proxychains", "tor", "obfs", "sleep", "history -c"] if k in cmd)
        recon_signals = sum(1 for k in ["nmap", "whois", "enum", "nikto", "dirb"] if k in cmd)
        credential_signals = sum(1 for k in ["hydra", "password", "sshpass", "login", "brute"] if k in cmd)

        repeats = 0.0
        if history_lower:
            repeats = sum(1 for item in history_lower[-10:] if item == cmd) / float(min(10, len(history_lower)))

        token_count = len(cmd.split())
        entropy_like = float(np.clip(np.std([ord(ch) for ch in cmd]) / 40.0 if cmd else 0.0, 0.0, 1.0))

        return [
            min(len(cmd) / 200.0, 1.0),
            min(token_count / 20.0, 1.0),
            min(typing_speed_cps / 12.0, 1.0),
            min(auto_signals / 4.0, 1.0),
            min(exploit_signals / 4.0, 1.0),
            min(opsec_signals / 3.0, 1.0),
            min(recon_signals / 4.0, 1.0),
            min(credential_signals / 4.0, 1.0),
            repeats,
            entropy_like,
        ]

    def _heuristic(self, command: str) -> str:
        cmd = command.lower()
        if any(k in cmd for k in ["masscan", "curl -s", "for i in", "bot", "scan"]):
            return "automated_bot"
        if any(k in cmd for k in ["hydra", "password", "admin:admin", "123456"]):
            return "script_kiddie"
        if any(k in cmd for k in ["nmap", "nikto", "burp", "sqlmap", "enum"]):
            return "pentester"
        if any(k in cmd for k in ["proxychains", "obfs", "living off the land", "powershell -enc", "cobalt"]):
            return "apt_actor"
        return "script_kiddie"

    def train(self, epochs: int = 140) -> None:
        if torch is None or nn is None or optim is None or self.model is None:
            self.is_trained = True
            return

        torch.manual_seed(9)

        samples = [
            ("hydra -l admin -P rockyou.txt ssh://10.0.0.1", 6.0, "script_kiddie"),
            ("masscan 10.0.0.0/8 -p22 --rate 10000", 18.0, "automated_bot"),
            ("nmap -sV -sC target", 4.2, "pentester"),
            ("proxychains nmap -sT target && sleep 3", 2.6, "apt_actor"),
            ("sqlmap -u http://app/item?id=1", 5.8, "pentester"),
            ("curl -s http://target/.env", 15.0, "automated_bot"),
            ("ssh admin@target", 3.9, "script_kiddie"),
            ("powershell -enc ZQB4AGUAYwA=", 2.0, "apt_actor"),
        ]

        x_data = []
        y_data = []
        for command, speed, label in samples:
            x_data.append(self._features(command=command, typing_speed_cps=speed, history=[]))
            y_data.append(ATTACK_LABELS.index(label))

        x = torch.tensor(x_data, dtype=torch.float32)
        y = torch.tensor(y_data, dtype=torch.long)

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.015)

        self.model.train()
        for _ in range(epochs):
            optimizer.zero_grad()
            logits = self.model(x)
            loss = criterion(logits, y)
            loss.backward()
            optimizer.step()

        self.is_trained = True

    def predict(self, command: str, typing_speed_cps: float, history: Sequence[str]) -> AttackClassification:
        if not self.is_trained:
            self.train()

        features = self._features(command=command, typing_speed_cps=typing_speed_cps, history=history)

        if torch is None or nn is None or optim is None or self.model is None:
            heuristic = self._heuristic(command)
            return AttackClassification(label=heuristic, confidence=0.75, feature_vector=features)

        x = torch.tensor([features], dtype=torch.float32)

        self.model.eval()
        with torch.no_grad():
            logits = self.model(x)
            probs = torch.softmax(logits, dim=1).squeeze(0)

        idx = int(torch.argmax(probs).item())
        label = ATTACK_LABELS[idx]
        confidence = float(probs[idx].item())

        heuristic = self._heuristic(command)
        if confidence < 0.66:
            label = heuristic
            confidence = max(confidence, 0.72)

        return AttackClassification(label=label, confidence=confidence, feature_vector=features)
