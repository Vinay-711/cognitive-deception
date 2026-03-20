# COGNITIVE DECEPTION

Autonomous Cyber Defense Intelligence Platform.

## Monorepo Structure

```text
cognitive-deception/
  backend/
    api/
    honeypot-engine/
    ai-modules/
    knowledge-graph/
    streaming/
    src/cognitive_deception/
    tests/
  frontend/
    app/
    components/
    pages/
    visualizations/
  infrastructure/
    docker/
    kubernetes/
    ci/
  scripts/
  docs/
```

## Capabilities Implemented

- AI deception engine with dynamic fake infrastructure and LLM decoy outputs
- Cognitive attacker profiling (typing speed, command patterns, tool signatures)
- Neuro-symbolic MITRE ATT&CK mapping and knowledge graph edge generation
- Synthetic corporate universe (employees, HR/finance docs, credentials, email/chat bait)
- AI-generated persona responses for social engineering probes
- Interactive terminal simulation APIs and full demo attack scenario
- Cyber intelligence metrics and report generation
- Docker Compose full stack (Postgres, Redis, Kafka, ElasticSearch, Neo4j, frontend, backend)
- Kubernetes deployment manifests + CI pipeline

## Quickstart (Local API)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
PYTHONPATH=src uvicorn cognitive_deception.api.main:app --reload --port 8000
```

## Full Stack (Docker)

```bash
./scripts/deploy_local.sh
```

Services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Neo4j Browser: http://localhost:7474
- ElasticSearch: http://localhost:9200

## Demo Mode (Hackathon)

```bash
./scripts/run_demo.sh
```

This triggers a simulated attacker session and generates a threat report.

## Backend API Endpoints

- `POST /api/v1/sessions/start`
- `POST /api/v1/sessions/{session_id}/command`
- `GET /api/v1/sessions/{session_id}/events`
- `GET /api/v1/dashboard/metrics`
- `POST /api/v1/demo/run`
- `POST /api/v1/reports/generate`
- `GET /api/v1/reports`

## Frontend

The frontend cyber command center is in `frontend/` with routes:
- `/`
- `/attacker-profile`
- `/deception-generator`
- `/simulation-console`
- `/report-center`

## Security Notes

- No sensitive keys are embedded in source.
- `.env.example` templates are provided.
- Command execution is simulated only.
- Recommend running in isolated network namespaces and restricted container policies for production.

## Reference Material

- Architecture: `docs/ARCHITECTURE.md`
- External intel/data sources: `docs/EXTERNAL_RESOURCES.md`
