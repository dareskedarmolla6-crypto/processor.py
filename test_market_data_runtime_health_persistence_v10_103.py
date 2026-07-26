from market.market_data_runtime import MarketDataRuntime
from market.in_memory_runtime_health_repository import (
    InMemoryRuntimeHealthRepository
)


class DummyScheduler:

    def run_once(self, symbols):
        return None


def test_runtime_persists_health():

    repo = InMemoryRuntimeHealthRepository()

    runtime = MarketDataRuntime(
        scheduler=DummyScheduler(),
        health_repository=repo
    )

    runtime.start()

    saved = repo.load_health()

    assert saved["status"] == "RUNNING"
    assert saved["cycles"] == 0


def test_runtime_restores_health():

    repo = InMemoryRuntimeHealthRepository()

    repo.save_health(
        {
            "status": "ERROR",
            "healthy": False,
            "cycles": 5,
            "last_error": "failure"
        }
    )

    runtime = MarketDataRuntime(
        scheduler=DummyScheduler(),
        health_repository=repo
    )

    health = runtime.health()

    assert health["status"] == "ERROR"
    assert health["cycles"] == 5
    assert health["last_error"] == "failure"
