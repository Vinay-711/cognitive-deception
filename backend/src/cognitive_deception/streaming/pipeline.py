from __future__ import annotations

import json
from asyncio import Queue
from contextlib import suppress
from typing import Any

from cognitive_deception.core.config import get_settings

try:
    from kafka import KafkaProducer
except Exception:  # pragma: no cover
    KafkaProducer = None

try:
    from elasticsearch import Elasticsearch
except Exception:  # pragma: no cover
    Elasticsearch = None


class EventPipeline:
    """Sensor telemetry pipeline: publishes to Kafka and indexes in Elastic with in-memory fallback."""

    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings

        self._producer = None
        self._elastic = None
        self.local_events: list[dict[str, Any]] = []
        self._subscribers: set[Queue] = set()

        if settings.enable_kafka and KafkaProducer is not None:
            try:
                self._producer = KafkaProducer(
                    bootstrap_servers=settings.kafka_bootstrap_servers,
                    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
                )
            except Exception:
                self._producer = None

        if settings.enable_elastic and Elasticsearch is not None:
            try:
                self._elastic = Elasticsearch(settings.elasticsearch_url)
            except Exception:
                self._elastic = None

    def publish_event(self, event: dict[str, Any]) -> None:
        self.local_events.append(event)
        self.local_events = self.local_events[-500:]

        for queue in list(self._subscribers):
            with suppress(Exception):
                queue.put_nowait(event)

        if self._producer is not None:
            try:
                self._producer.send(self.settings.kafka_topic, event)
                self._producer.flush(timeout=1)
            except Exception:
                pass

        if self._elastic is not None:
            try:
                self._elastic.index(index="cognitive-deception-events", document=event)
            except Exception:
                pass

    def latest(self, limit: int = 50) -> list[dict[str, Any]]:
        return self.local_events[-limit:]

    def subscribe(self, maxsize: int = 200) -> Queue:
        queue: Queue = Queue(maxsize=maxsize)
        self._subscribers.add(queue)
        return queue

    def unsubscribe(self, queue: Queue) -> None:
        self._subscribers.discard(queue)
