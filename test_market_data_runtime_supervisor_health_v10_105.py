from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)

from market.in_memory_runtime_health_repository import (
    InMemoryRuntimeHealthRepository
)


class DummyRuntime:

    def __init__(self):
        self._running = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def restart(self):
        self._running = True

        return {
            "status": "RUNNING"
        }

    def health(self):

        return {
            "status": "RUNNING",
            "healthy": True,
            "cycles": 1,
            "last_error": None
        }

    def state(self):

        return {
            "status": "RUNNING"
        }

    @property
    def running(self):
        return self._running



def test_supervisor_persists_health():

    runtime = DummyRuntime()

    repository = (
        InMemoryRuntimeHealthRepository()
    )

    supervisor = MarketDataRuntimeSupervisor(
        runtime,
        health_repository=repository
    )

    health = supervisor.check_health()

    saved = repository.load_health()

    assert health["status"] == "RUNNING"
    assert saved["status"] == "RUNNING"



def test_supervisor_start_updates_health():

    runtime = DummyRuntime()

    repository = (
        InMemoryRuntimeHealthRepository()
    )

    supervisor = MarketDataRuntimeSupervisor(
        runtime,
        health_repository=repository
    )

    supervisor.start()

    saved = repository.load_health()

    assert saved["healthy"] is True
