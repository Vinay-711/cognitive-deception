# Codebase Conventions

## Python Backend

### Code Style
- **Type hints**: Used throughout (`-> dict[str, str]`, `list[AttackEventRecord]`)
- **Imports**: `from __future__ import annotations` used in key files
- **String formatting**: f-strings preferred
- **Line length**: Generally ~120 chars (no explicit formatter config found)

### Patterns
- **Dependency injection**: FastAPI `Depends(get_db)` for database sessions
- **Singleton services**: `orchestrator = CognitiveDeceptionOrchestrator()` module-level instance
- **Config pattern**: `pydantic-settings` with `@lru_cache` for singleton config
- **Feature flags**: Boolean env vars (`ENABLE_KAFKA`, `ENABLE_REDIS`, etc.) gate optional services
- **Data classes**: `@dataclass` used for internal DTOs (`ProcessedEvent`)

### Error Handling
- **HTTP exceptions**: `HTTPException(status_code=404, detail="...")` for API errors
- **Resilience loop**: `backend/src/cognitive_deception/services/resilience.py` runs background health checks
- **Safety guards**: `max_command_length`, `max_session_events` config limits

### Module Organization
- Each AI module is a self-contained class with a `predict()` or `detect()` method
- Models split into: `entities.py` (SQLAlchemy), `schemas.py` (Pydantic), `db.py` (engine/session)
- Services follow single-responsibility: `deception_engine.py`, `persona_engine.py`, `synthetic_universe.py`

## TypeScript Frontend

### Code Style
- **Strict TypeScript**: enforced via tsconfig
- **React conventions**: functional components + hooks
- **Exports**: named exports (not default) in most files
- **State management**: React hooks (`useState`, `useEffect`) — no Redux/Zustand

### Patterns
- **Custom hooks**: `hooks/use-*.ts` files wrap API calls with loading/error state
- **API client**: centralized in `services/api-client.ts` with typed fetch wrappers
- **Component composition**: Shell → Page → Widgets → UI primitives
- **Styling**: Tailwind CSS + class-variance-authority (CVA) for variant-based styling
- **className helpers**: `cn()` utility combining `clsx` + `tailwind-merge` in `lib/utils.ts`

### Naming
- **Files**: kebab-case (`use-live-threat-stream.ts`)
- **Components**: PascalCase (`LiveActivityFeed`, `CyberCard`)
- **Hooks**: `use-` prefix for custom hooks
- **Types**: PascalCase, exported from API client or co-located
