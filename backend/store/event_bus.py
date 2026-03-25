import asyncio
from typing import Dict, List


class EventBus:
    def __init__(self):
        # Maps job_id -> list of asyncio Queues, one per connected SSE client
        self._subscribers: Dict[str, List[asyncio.Queue]] = {}
        # Tracks jobs that are fully done so late subscribers get immediate state
        self._completed: Dict[str, dict] = {}

    def subscribe(self, job_id: str) -> asyncio.Queue:
        queue: asyncio.Queue = asyncio.Queue()

        # If this job already completed, immediately enqueue its final state + done
        if job_id in self._completed:
            queue.put_nowait(self._completed[job_id])
            queue.put_nowait({"type": "done"})
            return queue

        if job_id not in self._subscribers:
            self._subscribers[job_id] = []
        self._subscribers[job_id].append(queue)
        return queue

    def unsubscribe(self, job_id: str, queue: asyncio.Queue) -> None:
        if job_id in self._subscribers:
            try:
                self._subscribers[job_id].remove(queue)
            except ValueError:
                pass
            if not self._subscribers[job_id]:
                del self._subscribers[job_id]

    async def publish(self, job_id: str, event: dict) -> None:
        queues = self._subscribers.get(job_id, [])
        for q in queues:
            await q.put(event)

    async def publish_done(self, job_id: str) -> None:
        # Store the done sentinel keyed by job so late subscribers can receive it
        queues = self._subscribers.pop(job_id, [])
        for q in queues:
            await q.put({"type": "done"})
        # Mark job_id as completed so future subscribers get instant response
        self._completed[job_id] = {"type": "done"}


event_bus = EventBus()
