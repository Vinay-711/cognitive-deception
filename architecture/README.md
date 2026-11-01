# Target Architecture

This directory describes the intended production-grade architecture and its mapping to the current codebase.

- Frontend: Next.js + Tailwind + Three.js
- Backend: FastAPI
- AI Engine: PyTorch + LangChain (planned) + vector DB
- Data Pipeline: Kafka / Redis Streams
- Threat Intelligence DB: PostgreSQL + pgvector
- Honeypot Layer: Cowrie, Dionaea, Custom Web Honeypot
- Orchestrator: Kubernetes

Use the repository’s root README and backend/frontend source to distinguish planned infrastructure from the current implementation.

## Source navigation

- [../backend/pyproject.toml](../backend/pyproject.toml)
- [../frontend/package.json](../frontend/package.json)

[Project setup and verification](../README.md). This directory guide describes the source boundary; deployment and external-service connectivity require their own checks.
