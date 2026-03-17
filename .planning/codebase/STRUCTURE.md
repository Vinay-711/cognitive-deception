# Codebase Structure

## Top-Level Layout

```
cognitive-deception/
├── ai_engine/              # Standalone AI modules (graph builder, classifiers, policy)
├── architecture/           # Architecture README placeholder
├── backend/                # Python FastAPI backend
│   ├── src/cognitive_deception/  # Main Python package
│   │   ├── ai/             # AI classification/prediction modules
│   │   ├── api/            # FastAPI routes + app setup
│   │   ├── core/           # Config, logging
│   │   ├── demo/           # Demo scenario runner
│   │   ├── knowledge/      # MITRE mapper + knowledge graph engine
│   │   ├── models/         # SQLAlchemy models + Pydantic schemas
│   │   ├── services/       # Business logic (orchestrator, deception, persona)
│   │   └── streaming/      # Event pipeline (in-memory pub/sub)
│   ├── tests/              # pytest test suite
│   ├── requirements.txt    # Python dependencies
│   └── pyproject.toml      # Build config + pytest settings
├── data/                   # Data files
├── datasets/               # Synthetic attack data generator + JSON
├── docs/                   # Architecture docs, API docs, deployment guide
├── frontend/               # Next.js 14 frontend
│   ├── app/                # App Router pages
│   ├── components/         # React components (nav, ui, visuals, widgets)
│   ├── hooks/              # Custom data-fetching hooks
│   ├── lib/                # Utility functions
│   ├── pages/              # Legacy pages dir (README only)
│   ├── services/           # API client + mock data
│   └── visualizations/     # Visualization components
├── honeypot/               # Honeypot configurations
├── infrastructure/         # Docker + K8s + CI
│   ├── ci/                 # GitHub Actions config
│   ├── docker/             # Dockerfiles + docker-compose.yml
│   └── kubernetes/         # K8s deployment manifests
└── scripts/                # Deployment and demo scripts
```

## Key Files

| File | Purpose |
|------|---------|
| `backend/src/cognitive_deception/api/main.py` | FastAPI app creation + lifespan |
| `backend/src/cognitive_deception/api/routes.py` | All REST + WebSocket endpoints |
| `backend/src/cognitive_deception/services/orchestrator.py` | Central orchestration logic |
| `backend/src/cognitive_deception/core/config.py` | Pydantic settings (env-based) |
| `backend/src/cognitive_deception/models/entities.py` | SQLAlchemy models |
| `backend/src/cognitive_deception/models/schemas.py` | Pydantic request/response schemas |
| `backend/src/cognitive_deception/models/db.py` | DB engine + session factory |
| `frontend/app/layout.tsx` | Root layout with AppShell |
| `frontend/app/page.tsx` | Landing page |
| `frontend/app/dashboard/page.tsx` | Main dashboard |
| `frontend/services/api-client.ts` | Typed API fetch wrappers |
| `frontend/components/shell/app-shell.tsx` | Navigation shell wrapper |
| `infrastructure/docker/docker-compose.yml` | Full stack service definitions |

## Naming Conventions

- **Backend packages**: snake_case (`cognitive_deception`, `attack_strategy_simulator`)
- **Frontend files**: kebab-case (`use-live-threat-stream.ts`, `cyber-card.tsx`)
- **Frontend components**: PascalCase exports (`SidebarNav`, `CyberCard`)
- **API routes**: REST-style with kebab-case paths (`/sessions/start`, `/dashboard/metrics`)
- **Config**: env vars are SCREAMING_SNAKE_CASE, settings fields are snake_case
