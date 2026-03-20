def test_demo_pipeline_flow(client):
    start = client.post(
        "/api/v1/sessions/start",
        json={"attacker_id": "demo-actor", "source_ip": "203.0.113.7", "channel": "ssh"},
    )
    assert start.status_code == 200
    session_id = start.json()["session_id"]

    cmd = client.post(
        f"/api/v1/sessions/{session_id}/command",
        json={"command": "hydra -l admin -P pass.txt ssh://10.0.0.7", "typing_duration_ms": 3400},
    )
    assert cmd.status_code == 200
    payload = cmd.json()

    assert payload["attack_label"] in {"script_kiddie", "automated_bot", "pentester", "apt_actor"}
    assert payload["mitre_technique"].startswith("T")
    assert payload["deception_strategy"] != ""

    metrics = client.get("/api/v1/dashboard/metrics")
    assert metrics.status_code == 200
    body = metrics.json()
    assert body["total_events"] >= 1

    report = client.post("/api/v1/reports/generate")
    assert report.status_code == 200
    assert "kill_chain_progression" in report.json()["report_json"]


def test_run_demo_scenario(client):
    result = client.post("/api/v1/demo/run")
    assert result.status_code == 200
    payload = result.json()

    assert payload["scenario_id"] == "demo-adaptive-honeypot-001"
    assert len(payload["steps"]) >= 3
