# API Reference

Base URL: `http://localhost:8000/api/v1`

## Sessions
- `POST /sessions/start`
- `POST /sessions/{session_id}/command`
- `GET /sessions/{session_id}/events`
- `GET /events/latest`

## Dashboard
- `GET /dashboard/metrics`

## Telemetry
- `GET /ws/telemetry` (WebSocket)

## Demo
- `POST /demo/run`

## Reports
- `POST /reports/generate`
- `GET /reports`
