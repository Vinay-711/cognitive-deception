# backend/streaming

Real-time pipeline path:
Honeypot sensors -> Kafka -> AI processing -> ElasticSearch -> Dashboard

Implemented in `backend/src/cognitive_deception/streaming/pipeline.py` with safe local fallback.
