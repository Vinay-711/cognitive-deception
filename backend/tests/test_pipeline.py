import asyncio

import pytest

from cognitive_deception.streaming.pipeline import EventPipeline


@pytest.mark.asyncio
async def test_pipeline_broadcasts():
    pipeline = EventPipeline()
    queue = pipeline.subscribe(maxsize=1)

    event = {"event_id": "evt-1", "type": "test"}
    pipeline.publish_event(event)

    received = await asyncio.wait_for(queue.get(), timeout=1)
    assert received["event_id"] == "evt-1"

    pipeline.unsubscribe(queue)
