from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

try:
    import numpy as np
except Exception:  # pragma: no cover
    np = None


@dataclass
class BehaviorSummary:
    cluster_id: int
    confidence: float
    features: list[float]


class BehaviorAnalyzer:
    """Behavior clustering and profiling.

    Uses a minimal k-means implementation for demo clustering.
    """

    def featurize(self, command: str, typing_speed_cps: float, repeats_ratio: float) -> list[float]:
        cmd = command.lower()
        return [
            min(len(cmd) / 200.0, 1.0),
            min(len(cmd.split()) / 20.0, 1.0),
            min(typing_speed_cps / 12.0, 1.0),
            repeats_ratio,
            float("sqlmap" in cmd or "payload" in cmd),
            float("hydra" in cmd or "password" in cmd),
            float("nmap" in cmd or "scan" in cmd),
        ]

    def cluster(self, features: Iterable[list[float]], k: int = 3) -> list[int]:
        if np is None:
            return [0 for _ in features]
        x = np.array(list(features), dtype=float)
        if x.size == 0:
            return []
        centers = x[:k].copy()
        for _ in range(8):
            distances = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)
            labels = distances.argmin(axis=1)
            for idx in range(k):
                cluster = x[labels == idx]
                if cluster.size:
                    centers[idx] = cluster.mean(axis=0)
        return labels.tolist()

    def analyze(self, command: str, typing_speed_cps: float, repeats_ratio: float) -> BehaviorSummary:
        features = self.featurize(command, typing_speed_cps, repeats_ratio)
        cluster_id = self.cluster([features], k=3)[0] if np is not None else 0
        confidence = 0.72 if cluster_id == 0 else 0.78
        return BehaviorSummary(cluster_id=cluster_id, confidence=confidence, features=features)
