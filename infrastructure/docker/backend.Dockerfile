FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY backend /app/backend
WORKDIR /app/backend

ENV PYTHONPATH=/app/backend/src

EXPOSE 8000

CMD ["uvicorn", "cognitive_deception.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
