from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DeceptionProfile:
    strategy: str
    state: dict[str, Any]


class DeceptionEngine:
    """Adaptive environment generator that changes fake assets as attacker strategy shifts."""

    PROFILE_MAP = {
        "baseline_obfuscation": {
            "filesystem": "corp-linux-gateway",
            "service_banner": "OpenSSH_8.2p1 Ubuntu-4ubuntu0.5",
            "fake_services": ["jira.internal", "git.internal", "hr-portal"],
            "fake_vulns": ["OutdatedTLSMarker"],
        },
        "surface_expansion": {
            "filesystem": "legacy-lab-segment",
            "service_banner": "OpenSSH_7.2p2 Ubuntu-4ubuntu2.8",
            "fake_services": ["legacy-vpn", "kibana-archive", "old-inventory"],
            "fake_vulns": ["CVE-2019-19781", "CVE-2021-41773"],
        },
        "credential_sinkhole": {
            "filesystem": "auth-admin-node",
            "service_banner": "OpenSSH_6.6.1p1",
            "fake_services": ["ad-sync", "sso-admin", "password-reset"],
            "fake_vulns": ["WeakPasswordPolicy"],
        },
        "vulnerability_mirage": {
            "filesystem": "dmz-web-cluster",
            "service_banner": "Apache/2.2.15",
            "fake_services": ["billing-api-v1", "legacy-reporting", "cms-admin"],
            "fake_vulns": ["CVE-2022-1388", "CVE-2021-44228"],
        },
        "deep_persona_diversion": {
            "filesystem": "executive-data-vault",
            "service_banner": "OpenSSH_5.3p1",
            "fake_services": ["board-portal", "mna-data-room", "wire-transfer-ops"],
            "fake_vulns": ["PrivilegedBackupMisconfig"],
        },
    }

    def apply(self, strategy: str, universe: dict[str, Any]) -> DeceptionProfile:
        base = dict(self.PROFILE_MAP.get(strategy, self.PROFILE_MAP["baseline_obfuscation"]))
        base["honey_files"] = universe.get("files", [])[:3]
        base["honey_credentials"] = universe.get("credentials", [])[:2]
        return DeceptionProfile(strategy=strategy, state=base)
