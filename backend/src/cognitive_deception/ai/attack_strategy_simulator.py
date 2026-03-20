from dataclasses import dataclass


@dataclass
class StrategyDecision:
    strategy: str
    risk_score: float
    rationale: str


class AttackStrategySimulator:
    """Maps attacker profile + threat pattern into adaptive deception strategy."""

    def decide(self, attack_label: str, bias: str, exploit_pattern: str, severity: float) -> StrategyDecision:
        if attack_label == "apt_actor" and severity > 0.8:
            return StrategyDecision(
                strategy="deep_persona_diversion",
                risk_score=92.0,
                rationale="High-capability actor with elevated exploit severity",
            )

        if exploit_pattern in {"credential_attack", "repetitive_scanning"}:
            return StrategyDecision(
                strategy="credential_sinkhole",
                risk_score=74.0,
                rationale="Credential-focused behavior redirected to controlled lure accounts",
            )

        if bias == "reconnaissance_pattern":
            return StrategyDecision(
                strategy="surface_expansion",
                risk_score=66.0,
                rationale="Recon workflow should be fed with broadened fake infrastructure",
            )

        if exploit_pattern == "exploit_injection":
            return StrategyDecision(
                strategy="vulnerability_mirage",
                risk_score=84.0,
                rationale="Exploit probes trigger synthetic vulnerable services",
            )

        return StrategyDecision(
            strategy="baseline_obfuscation",
            risk_score=52.0,
            rationale="Default deception posture for low signal interactions",
        )
