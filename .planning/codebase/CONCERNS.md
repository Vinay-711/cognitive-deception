# Codebase Concerns

## Technical Debt

### 1. Singleton Orchestrator Initialization
- `orchestrator = CognitiveDeceptionOrchestrator()` is instantiated at module import time
- Calls `self.behavior.train()` during `__init__`, causing import-time side effects
- Makes testing harder — every import triggers model training
- **Location**: `backend/src/cognitive_deception/services/orchestrator.py:233`

### 2. No Frontend Tests
- Zero test files in `frontend/`
- No test framework configured
- All frontend validation is manual
- **Risk**: Regressions go undetected as UI grows

### 3. Mock Data Remnants
- `frontend/services/mock-data.ts` exists alongside real API client
- Previous conversations indicate ongoing effort to replace mocks with real data
- Some hooks/components may still fall back to mock data

### 4. Duplicate AI Modules
- `ai_engine/` (top-level, standalone) overlaps with `backend/src/cognitive_deception/ai/`
- Both contain behavior classifiers and attack pattern logic
- Unclear which is the canonical source of truth
- **Files**: `ai_engine/behavior_classifier.py` vs `backend/src/cognitive_deception/ai/behavior_classifier.py`

### 5. Heavy Python Dependencies
- PyTorch `2.10.0` is pulled for relatively simple classification tasks
- Could likely use sklearn or rule-based approaches to reduce container size significantly

## Security Concerns

### 1. Default Credentials in Docker Compose
- `infrastructure/docker/docker-compose.yml` contains hardcoded passwords:
  - Postgres: `cognitive/secret`
  - Neo4j: `neo4j/changeme`
- `.env.example` templates should be used with proper secrets management

### 2. No Authentication on API
- All REST endpoints are unauthenticated
- No auth middleware, API keys, or JWT tokens
- WebSocket telemetry endpoint is open
- Fine for demo/dev but critical for any deployment

### 3. CORS Configuration Missing
- No CORS middleware configured in `main.py`
- Frontend-backend communication may break in production deployments

## Performance Concerns

### 1. N+1 Queries in Routes
- `routes.py` metrics endpoint loads ALL sessions and ALL events into memory
- `Counter()` aggregation done in Python instead of SQL
- **Location**: `backend/src/cognitive_deception/api/routes.py:139-163`

### 2. No Pagination
- `/events/latest` has a `limit` param but most endpoints load all records
- `/dashboard/metrics` scans full tables
- Will not scale with large event volumes

### 3. Synchronous DB Operations
- SQLAlchemy configured with synchronous engine despite FastAPI's async nature
- Could benefit from async SQLAlchemy or at least `run_in_threadpool`

## Fragile Areas

### 1. Event Pipeline In-Memory Only
- `streaming/pipeline.py` uses in-memory pub/sub
- Events are lost on server restart
- Kafka integration is scaffolded but disabled by default

### 2. Geolocation Service
- `services/geolocation.py` called on every command processing
- Likely uses fake/static data for simulated IPs
- Could become a bottleneck if pointed at external API

### 3. LLM Fallback Path
- When `USE_LLM=false`, `llm_deception_generator.py` uses template responses
- Quality difference between LLM and template modes may be significant
- No clear indication to users which mode is active
