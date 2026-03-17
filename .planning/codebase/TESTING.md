# Codebase Testing

## Backend Testing

### Framework
- **pytest** `8.4.1` + **pytest-asyncio** `1.1.0`
- Config: `backend/pyproject.toml` → `[tool.pytest.ini_options]`
  - `pythonpath = ["src"]`
  - `addopts = "-q"`

### Test Setup (`backend/tests/conftest.py`)
- Uses SQLite in-memory test DB at `/tmp/test_cognitive_deception.db`
- All optional services disabled via env vars (`USE_LLM=false`, `ENABLE_KAFKA=false`, etc.)
- **Fixtures**:
  - `setup_db` (session-scoped) — creates/drops all tables
  - `clean_db` (auto-use) — truncates tables between tests
  - `client` — FastAPI `TestClient` with DB override

### Test Files
| File | Coverage Area |
|------|---------------|
| `backend/tests/test_api_flow.py` | Full API flow: session start → command → events |
| `backend/tests/test_ai_modules.py` | AI module predict/detect methods |
| `backend/tests/test_pipeline.py` | Event pipeline pub/sub |
| `backend/tests/test_resilience.py` | Resilience loop and health checks |

### Running Tests
```bash
cd backend
source .venv/bin/activate
pytest
```

## Frontend Testing

- No test framework currently configured
- No test files present in `frontend/`
- `package.json` has no `test` script

## Type Checking

| Tool | Config | Scope |
|------|--------|-------|
| Pyre | `.pyre_configuration` | Python backend |
| Pyright | `backend/pyrightconfig.json` | Python backend |
| TypeScript | `frontend/tsconfig.json` | Frontend |
| ESLint | `frontend/eslint-config-next` | Frontend linting |
