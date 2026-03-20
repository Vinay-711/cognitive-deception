# Cognitive Adaptive Honeypot – Debug Report

Generated: 2026-03-16

## Summary
This audit focused on correctness, runtime stability, dependency health, and security posture. I ran backend tests, frontend build/lint/typecheck, and inspected configs and runtime flow. The system is functional end-to-end, but several issues were found that affect developer experience, linting, and security hardening. All items marked **Fixed** are already repaired in the repo.

## Findings

### 1) ESLint/Next.js version mismatch (Frontend)
- **Severity**: High (blocks `npm run lint` and Next build lint stage)
- **Root cause**: `eslint` v9 and `eslint-config-next` v16 were installed with Next 14.2.5, causing Next lint to fail with invalid option errors.
- **Location**: `frontend/package.json`
- **Fix**: Pin ESLint to v8 and `eslint-config-next` to `14.2.5`.
- **Status**: **Fixed**

### 2) TypeScript typecheck fails on clean checkout (Frontend)
- **Severity**: Medium (blocks `tsc --noEmit` unless a build is run first)
- **Root cause**: Next.js writes `.next/types/**/*.ts` into `tsconfig.json`, but those files are not present before a build. This causes `TS6053` errors when running `tsc` directly.
- **Location**: `frontend/tsconfig.json`, `frontend/package.json`
- **Fix**: Use `next build` as the canonical `typecheck` command so `.next/types` is generated first.
- **Status**: **Fixed**

### 3) Missing ESLint config (Frontend)
- **Severity**: Medium
- **Root cause**: No `.eslintrc` present, so `next lint` prompted for interactive setup.
- **Location**: `frontend/.eslintrc.json`
- **Fix**: Add minimal Next core-web-vitals ESLint config.
- **Status**: **Fixed**

### 4) Backend venv lacked dependencies (Backend)
- **Severity**: High (tests and modules failed to import)
- **Root cause**: `backend/.venv` existed but didn’t have `requirements.txt` installed (missing `pytest`, `numpy`, etc.).
- **Location**: `backend/.venv`
- **Fix**: Install `requirements.txt` in the venv.
- **Status**: **Fixed**

### 5) Default secrets in config (Security)
- **Severity**: High (security risk)
- **Root cause**: Default Neo4j password set to `changeme` and used in Docker/K8s configs.
- **Location**: `backend/src/cognitive_deception/core/config.py`, `infrastructure/docker/docker-compose.yml`, `infrastructure/kubernetes/data-services.yaml`
- **Fix**: Use secrets manager or env overrides in production, and rotate defaults for demos.
- **Status**: **Open** (documented; not changed to avoid breaking demo environments)

### 6) LLM usage disabled by default
- **Severity**: Low (feature not active, not a runtime error)
- **Root cause**: `USE_LLM=false` defaults to fallback response logic.
- **Location**: `backend/src/cognitive_deception/core/config.py`, `backend/.env.example`
- **Fix**: Provide `OPENAI_API_KEY` and set `USE_LLM=true` to enable real LLM output.
- **Status**: **Open** (expected for safe defaults)

### 7) Service mismatch between local default DB and infra
- **Severity**: Medium
- **Root cause**: Backend defaults to SQLite, while infrastructure defines Redis/Kafka/Elastic/Neo4j. No migration path or Postgres/pgvector in current code.
- **Location**: `backend/src/cognitive_deception/core/config.py`, `infrastructure/docker/docker-compose.yml`
- **Fix**: Add PostgreSQL + pgvector service and update SQLAlchemy URL and models or add migration scripts.
- **Status**: **Open** (requires schema/driver changes)

### 8) Frontend dependency bloat and unused packages
- **Severity**: Low
- **Root cause**: `@deck.gl/*` and `mapbox-gl` remain in `package.json` though current UI uses SVG fallback.
- **Location**: `frontend/package.json`
- **Fix**: Remove unused dependencies if not planning to re-enable Deck.gl.
- **Status**: **Open**

### 9) Python 3.14 deprecation warnings
- **Severity**: Low
- **Root cause**: Third-party libs (FastAPI/Neo4j) call `asyncio.iscoroutinefunction`, deprecated in 3.14.
- **Location**: `.venv` packages
- **Fix**: Upgrade dependencies when they adopt `inspect.iscoroutinefunction`.
- **Status**: **Open** (non-blocking warnings)

## Test Results
- Backend: `pytest` passed (4 tests).
- Frontend: `npm run build` passed.
- Frontend: `npm run lint` passed.
- Frontend: `npm run typecheck` passed.

## Recommendations
- Introduce PostgreSQL + pgvector for production (per target architecture), and migrate from SQLite.
- Add a secrets policy for all credentials in Docker/K8s.
- Consider pruning unused UI dependencies to reduce attack surface.
- Add explicit migration + seed scripts for consistent demo state.
