# Deployment Guide

## Local
Backend:
```
cd backend
source .venv/bin/activate
export PYTHONPATH=src
uvicorn cognitive_deception.api.main:app --reload --port 8000
```

Frontend:
```
cd frontend
npm run dev:clean
```

## Docker Compose
```
docker compose -f infrastructure/docker/docker-compose.yml up --build
```

## Services & Ports
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Backend Docs: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`
- Kafka: `localhost:9092`
- Redis: `localhost:6379`
- Elasticsearch: `localhost:9200`
- Neo4j: `localhost:7474`
- Cowrie emulation: `localhost:2222`
- Dionaea emulation: `localhost:4444`
- Web honeypot: `http://localhost:8081`

## Environment
- Backend: `backend/.env.example`
- Frontend: `frontend/.env.example`
