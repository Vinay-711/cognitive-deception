from dataclasses import dataclass


@dataclass
class BiasPrediction:
    bias: str
    score: float
    rationale: str


class CognitiveBiasPredictor:
    """Estimates attacker cognitive bias from command rhythm and intent patterns."""

    def predict(self, command: str, typing_speed_cps: float, repeats_ratio: float, attack_label: str) -> BiasPrediction:
        cmd = command.lower()

        if repeats_ratio > 0.5 or "retry" in cmd:
            return BiasPrediction(
                bias="time_pressure",
                score=0.83,
                rationale="Repeated rapid attempts indicate urgency-driven behavior",
            )

        if attack_label in {"script_kiddie", "automated_bot"} and any(k in cmd for k in ["admin", "root", "default"]):
            return BiasPrediction(
                bias="confirmation_bias",
                score=0.76,
                rationale="Default credential assumptions suggest pre-decided hypothesis",
            )

        if attack_label in {"pentester", "apt_actor"} and any(k in cmd for k in ["nmap", "enum", "whois", "dirb"]):
            return BiasPrediction(
                bias="reconnaissance_pattern",
                score=0.88,
                rationale="Structured reconnaissance workflow observed",
            )

        if typing_speed_cps < 2.8 and attack_label == "apt_actor":
            return BiasPrediction(
                bias="overconfidence",
                score=0.71,
                rationale="Deliberate operator behavior with stealth assumptions",
            )

        return BiasPrediction(
            bias="overconfidence",
            score=0.64,
            rationale="Fallback bias from confident probing behavior",
        )
