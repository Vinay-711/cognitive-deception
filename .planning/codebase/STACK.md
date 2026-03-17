# Codebase Stack

## Languages & Runtimes

| Language | Version | Location |
|----------|---------|----------|
| Python | ≥3.11 | `backend/` |
| TypeScript | ^5.7 | `frontend/` |
| SQL | PostgreSQL 16 | `infrastructure/docker/postgres/init.sql` |
| YAML | — | `infrastructure/`, `.github/workflows/` |

## Backend Framework

- **FastAPI** `0.116.1` — async REST API + WebSocket support
- **Uvicorn** `0.35.0` — ASGI server with standard extras
- **Pydantic** `2.12.5` + **pydantic-settings** `2.10.1` — model validation & env-based config
- **SQLAlchemy** `2.0.43` — ORM with declarative base pattern
- Entry point: `backend/src/cognitive_deception/api/main.py`
- Config: `backend/src/cognitive_deception/core/config.py` (pydantic BaseSettings, `.env` file)

## Frontend Framework

- **Next.js** `14.2.5` (App Router)
- **React** `18.3.1` + **React DOM** `18.3.1`
- **Tailwind CSS** `^3.4.17` — utility-first styling
- **Framer Motion** `^11.18.2` — animations
- **Recharts** `^2.15.1` — data visualization charts
- **Three.js** `^0.172.0` + `@react-three/fiber` + `@react-three/drei` — 3D visualizations
- **Mapbox GL** `^3.20.0` + `react-map-gl` — geo threat maps
- **deck.gl** `^9.2.2` — large-scale data visualization layers
- **Lucide React** `^0.468.0` — icons
- **Radix UI** — headless components (progress, select)
- **CVA** + **clsx** + **tailwind-merge** — className management

## AI / ML Stack

- **PyTorch** `2.10.0` — ML model inference (behavior classification)
- **NumPy** `2.3.2` — numerical processing
- Custom AI modules in `backend/src/cognitive_deception/ai/`:
  - `behavior_classifier.py` — sklearn-style classifier trained on-init
  - `cognitive_bias_predictor.py` — rule-based bias analysis
  - `threat_pattern_detector.py` — regex + heuristic threat patterns
  - `attack_strategy_simulator.py` — deception strategy selection
  - `llm_deception_generator.py` — OpenAI-backed response generation (optional)
- Standalone AI engine: `ai_engine/` — graph builder, intent predictor, policy engine

## Data Layer

| System | Library | Version | Purpose |
|--------|---------|---------|---------|
| PostgreSQL | `psycopg2-binary` | `2.9.10` | Primary relational DB |
| pgvector | `pgvector` | `0.3.6` | Vector similarity search |
| Redis | `redis` | `6.4.0` | Caching / pub-sub |
| Elasticsearch | `elasticsearch` | `8.15.1` | Full-text search / log indexing |
| Neo4j | `neo4j` | `5.28.2` | Knowledge graph |
| Kafka | `kafka-python` | `2.1.2` | Event streaming |
| SQLite | built-in | — | Local dev fallback DB |

## HTTP Client

- **httpx** `0.28.1` — async HTTP client for external API calls

## Build & Dev Tools

| Tool | Config File |
|------|-------------|
| setuptools | `backend/pyproject.toml` |
| pytest | `backend/pyproject.toml` ([tool.pytest.ini_options]) |
| ESLint | `frontend/.eslintrc*` (next config) |
| PostCSS | `frontend/postcss.config.js` |
| TypeScript | `frontend/tsconfig.json` |
| Pyre | `.pyre_configuration` (Python type checker) |
| Pyright | `backend/pyrightconfig.json` |

## Configuration

- Backend config via `pydantic-settings`: reads `.env` file with `SettingsConfigDict`
- Feature flags: `ENABLE_KAFKA`, `ENABLE_ELASTIC`, `ENABLE_NEO4J`, `ENABLE_REDIS`, `USE_LLM`
- Frontend env: `NEXT_PUBLIC_API_BASE_URL` defaults to `http://localhost:8000/api/v1`
