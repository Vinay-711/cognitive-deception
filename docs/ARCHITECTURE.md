# Cognitive Adaptive Deception System – Architecture

## Layers
1. Cognitive Deception Layer
2. Adaptive Honeypot Infrastructure
3. AI Behavioral Analysis Engine
4. Threat Intelligence Pipeline
5. Visualization Dashboard

## Stack
- Frontend: Next.js + Tailwind + Three.js
- Backend: FastAPI
- AI Engine: PyTorch + LangChain (scaffolded)
- Database: PostgreSQL + pgvector
- Streaming: Kafka + in-memory WebSocket relay
- Honeypot Layer: Cowrie (emulated), Dionaea (emulated), Custom Web Honeypot
- Deployment: Docker + Docker Compose

## Component Map
- API: `backend/src/cognitive_deception/api/*`
- Orchestrator: `backend/src/cognitive_deception/services/orchestrator.py`
- AI Modules: `backend/src/cognitive_deception/ai/*` + `ai_engine/*`
- Streaming: `backend/src/cognitive_deception/streaming/*`
- Telemetry: `/api/v1/ws/telemetry`
- Frontend: `frontend/*`

## Data Flow
1. Honeypot event → backend `/sessions/start` + `/sessions/{id}/command`
2. Orchestrator → classifier + bias + strategy
3. MITRE mapping + deception profile
4. Event stored in Postgres + broadcast via pipeline
5. Dashboard consumes `/dashboard/metrics` + WebSocket

## Security Posture
- Isolation at container boundary
- No live command execution
- Telemetry only, safe output generation
