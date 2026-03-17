# Codebase Architecture

## Architecture Pattern

**Layered Monolith** with service-oriented internal structure. The backend is a monolithic FastAPI application organized into distinct layers, with optional external service integrations feature-flagged.

## Layers

```
┌──────────────────────────────────┐
│       Frontend (Next.js)         │  React components + data hooks
├──────────────────────────────────┤
│   REST API / WebSocket Layer     │  FastAPI routes + Pydantic schemas
├──────────────────────────────────┤
│       Orchestrator               │  CognitiveDeceptionOrchestrator
├──────────────┬───────────────────┤
│  AI Modules  │  Services Layer   │  Classifiers + Deception/Persona engines
├──────────────┼───────────────────┤
│  Knowledge   │  Streaming        │  MITRE mapper + graph + event pipeline
├──────────────┴───────────────────┤
│       Data Layer (SQLAlchemy)    │  Postgres/SQLite + optional Redis/ES/Neo4j/Kafka
└──────────────────────────────────┘
```

## Key Abstractions

### Orchestrator (`backend/src/cognitive_deception/services/orchestrator.py`)
Central coordinator — singleton `orchestrator` instance. Composes all AI modules, services, and knowledge layers. Processes every command through a pipeline:
1. Behavior classification
2. Pattern detection
3. Cognitive bias prediction
4. Strategy simulation
5. MITRE ATT&CK mapping
6. Deception response generation
7. Event storage + streaming

### AI Module Pattern
Each AI module follows a predict/detect/decide interface:
- `BehaviorClassifier.predict(command, typing_speed, history)` → classification
- `ThreatPatternDetector.detect(command, history)` → pattern + severity
- `CognitiveBiasPredictor.predict(...)` → bias + score + rationale
- `AttackStrategySimulator.decide(...)` → strategy + risk_score
- `LLMDeceptionGenerator.generate(...)` → deception response text

### Data Flow

```
Honeypot Event → POST /sessions/{id}/command
    → orchestrator.process_command()
        → BehaviorClassifier.predict()
        → ThreatPatternDetector.detect()
        → CognitiveBiasPredictor.predict()
        → AttackStrategySimulator.decide()
        → MitreMapper.map_pattern()
        → DeceptionEngine.apply()
        → PersonaEngine / LLMDeceptionGenerator
        → AttackEvent stored in DB
        → EventPipeline.publish_event()
        → KnowledgeGraphEngine.record_attack_edge()
    → Response returned to honeypot/client
```

### Frontend Architecture
- **App Router** (Next.js 14) with page-based routing
- **Custom hooks** (`frontend/hooks/`) fetch data from backend API
- **Shell pattern**: `components/shell/app-shell.tsx` wraps all pages
- **Component categories**:
  - `components/nav/` — sidebar navigation
  - `components/ui/` — reusable UI primitives (card, button, badge, progress)
  - `components/visuals/` — data visualizations (network graph, threat map, timeline)
  - `components/widgets/` — dashboard widgets (MITRE mapping, traffic viz, terminal)
- **Services**: `frontend/services/api-client.ts` — typed API fetch functions

## Entry Points

| Entry Point | Location |
|-------------|----------|
| Backend API | `backend/src/cognitive_deception/api/main.py` |
| Frontend | `frontend/app/layout.tsx` + `frontend/app/page.tsx` |
| Demo runner | `backend/src/cognitive_deception/demo/scenario_runner.py` |
| Tests | `backend/tests/conftest.py` |
| Docker stack | `infrastructure/docker/docker-compose.yml` |
| CI pipeline | `.github/workflows/ci.yml` |
