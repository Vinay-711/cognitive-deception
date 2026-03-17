# Codebase Integrations

## External Services

### PostgreSQL (pgvector)
- **Purpose**: Primary relational database for sessions, events, reports
- **Config**: `DATABASE_URL` env var, defaults to SQLite for local dev
- **Docker**: `pgvector/pgvector:pg16` image with init script at `infrastructure/docker/postgres/init.sql`
- **ORM**: SQLAlchemy declarative base in `backend/src/cognitive_deception/models/db.py`

### Redis
- **Purpose**: Caching and pub/sub (feature-flagged)
- **Config**: `REDIS_URL`, `ENABLE_REDIS` env vars
- **Docker**: `redis:7-alpine`
- **Usage**: Optional — disabled by default in local dev

### Apache Kafka
- **Purpose**: Event streaming pipeline for honeypot events
- **Config**: `KAFKA_BOOTSTRAP_SERVERS`, `KAFKA_TOPIC`, `ENABLE_KAFKA`
- **Docker**: `bitnami/kafka:3.7` + `bitnami/zookeeper:3.9`
- **Usage**: Optional — disabled in local/test mode

### Elasticsearch
- **Purpose**: Full-text search and log indexing for attack events
- **Config**: `ELASTICSEARCH_URL`, `ENABLE_ELASTIC`
- **Docker**: `docker.elastic.co/elasticsearch/elasticsearch:8.15.1`
- **Usage**: Optional — disabled in local/test mode

### Neo4j
- **Purpose**: Knowledge graph for attack relationships (attacker→tool→technique→target)
- **Config**: `NEO4J_URI`, `NEO4J_USER`, `NEO4J_PASSWORD`, `ENABLE_NEO4J`
- **Docker**: `neo4j:5.24`
- **Code**: `backend/src/cognitive_deception/knowledge/graph_engine.py`
- **Usage**: Optional — records attack edges when enabled

### OpenAI API
- **Purpose**: LLM-powered deception response generation
- **Config**: `OPENAI_API_KEY`, `OPENAI_MODEL` (defaults to `gpt-4o-mini`), `USE_LLM`
- **Code**: `backend/src/cognitive_deception/ai/llm_deception_generator.py`
- **Usage**: Optional — falls back to template-based responses when disabled

## Internal APIs

### REST API (`/api/v1`)
- **Entry**: `backend/src/cognitive_deception/api/routes.py`
- **Endpoints**:
  - `POST /sessions/start` — create attack session
  - `POST /sessions/{id}/command` — process attacker command  
  - `GET /sessions/{id}/events` — session event history
  - `GET /events/latest` — recent events feed
  - `GET /dashboard/metrics` — aggregated metrics
  - `POST /demo/run` — demo scenario
  - `POST /reports/generate` — threat report
  - `GET /reports` — list reports
  - `GET /deception` — deception session overviews
  - `GET /attacks` — attack feed
  - `GET /analysis` — analysis summary
  - `GET /network` — network graph data

### WebSocket (`/api/v1/ws/telemetry`)
- Real-time event streaming to frontend
- Pub/sub via in-memory `EventPipeline`
- Code: `backend/src/cognitive_deception/streaming/pipeline.py`

### Frontend → Backend
- API client: `frontend/services/api-client.ts`
- Typed fetch wrappers for all REST endpoints
- Base URL: `NEXT_PUBLIC_API_BASE_URL` env var

## Honeypot Services (Docker)
- **Cowrie** (SSH honeypot): port 2222, reports to backend API
- **Dionaea** (TCP honeypot): port 4444, reports to backend API
- **Web Honeypot** (HTTP): port 8081, reports to backend API
- All built from `infrastructure/docker/honeypot.Dockerfile`

## CI/CD
- **GitHub Actions**: `.github/workflows/ci.yml`
- **Kubernetes**: deployment manifests in `infrastructure/kubernetes/`
