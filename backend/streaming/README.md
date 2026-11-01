# backend/streaming

Real-time pipeline path:
Honeypot sensors -> Kafka -> AI processing -> ElasticSearch -> Dashboard

Implemented in `backend/src/cognitive_deception/streaming/pipeline.py` with safe local fallback.

## Source navigation

- [../src/cognitive_deception/streaming/pipeline.py](../src/cognitive_deception/streaming/pipeline.py)

[Project setup and verification](../../README.md). This directory guide describes the source boundary; deployment and external-service connectivity require their own checks.
