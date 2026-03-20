from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DeceptionPolicy:
    strategy: str
    rationale: str


class DeceptionPolicyEngine:
    """Maps attacker intent + behavior to deception strategies.

    This is designed to be replaced by RL policies later. For now it is rule-based
    so it remains deterministic in demos and tests.
    """

    def decide(self, behavior_label: str, intent: str) -> DeceptionPolicy:
        if intent == "credential_access":
            return DeceptionPolicy("credential_sinkhole", "Redirect brute-force to bait credentials")
        if intent == "exploit":
            return DeceptionPolicy("vulnerability_mirage", "Expose synthetic vulnerable services")
        if intent == "reconnaissance":
            return DeceptionPolicy("surface_expansion", "Increase attack surface with decoys")
        if behavior_label == "apt_actor":
            return DeceptionPolicy("deep_persona_diversion", "High sophistication -> deep persona lure")
        return DeceptionPolicy("baseline_obfuscation", "Default deception posture")
