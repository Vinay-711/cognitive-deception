from __future__ import annotations

from dataclasses import dataclass
from random import random


@dataclass
class StrategyDecision:
    strategy: str
    score: float
    rationale: str


class DeceptionStrategyEngine:
    """Simple RL-inspired policy engine with epsilon-greedy updates."""

    def __init__(self) -> None:
        self.q = {}
        self.epsilon = 0.15

    def _key(self, behavior: str, intent: str) -> str:
        return f"{behavior}:{intent}"

    def decide(self, behavior: str, intent: str) -> StrategyDecision:
        key = self._key(behavior, intent)
        candidates = self.q.get(key, {"baseline_obfuscation": 0.5})

        if random() < self.epsilon:
            strategy = "baseline_obfuscation"
            score = 0.5
            rationale = "epsilon exploration"
        else:
            strategy = max(candidates, key=candidates.get)
            score = candidates[strategy]
            rationale = "highest expected reward"

        return StrategyDecision(strategy=strategy, score=score, rationale=rationale)

    def update(self, behavior: str, intent: str, strategy: str, reward: float) -> None:
        key = self._key(behavior, intent)
        if key not in self.q:
            self.q[key] = {strategy: reward}
        else:
            self.q[key][strategy] = (self.q[key].get(strategy, 0.0) * 0.7) + (reward * 0.3)
