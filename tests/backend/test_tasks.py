from __future__ import annotations

from source.modules.tasks import TaskQueue


class _FakeWorker:
    def __init__(self, running: bool = True):
        self._running = running
        self.fullstop_called = False

    def isRunning(self) -> bool:
        return self._running

    def fullstop(self) -> None:
        self.fullstop_called = True


def test_fullstop_disables_thread_respawn():
    queue = TaskQueue(worker_count=0)
    worker = _FakeWorker()
    queue.workers[worker] = None

    queue.fullstop()

    assert queue._making_threads is False
    assert worker.fullstop_called is True
