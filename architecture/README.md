# Target Architecture

This directory describes the intended production-grade architecture and its mapping to the current codebase.

- Frontend: Next.js + Tailwind + Three.js
- Backend: FastAPI
- AI Engine: PyTorch + LangChain (planned) + vector DB
- Data Pipeline: Kafka / Redis Streams
- Threat Intelligence DB: PostgreSQL + pgvector
- Honeypot Layer: Cowrie, Dionaea, Custom Web Honeypot
- Orchestrator: Kubernetes

See `docs/architecture.md` for the full plan and staging guidance.
