from dataclasses import dataclass


@dataclass
class MitreMapping:
    technique_id: str
    technique_name: str


class MitreMapper:
    MAP = {
        "reconnaissance": ("T1595", "Active Scanning"),
        "credential_attack": ("T1110", "Brute Force"),
        "exploit_injection": ("T1190", "Exploit Public-Facing Application"),
        "exfiltration": ("T1041", "Exfiltration Over C2 Channel"),
        "repetitive_scanning": ("T1595", "Active Scanning"),
        "low_signal": ("T1059", "Command and Scripting Interpreter"),
    }

    def map_pattern(self, exploit_pattern: str) -> MitreMapping:
        technique_id, technique_name = self.MAP.get(exploit_pattern, ("T1059", "Command and Scripting Interpreter"))
        return MitreMapping(technique_id=technique_id, technique_name=technique_name)
