from market.market_data_runtime import MarketDataRuntime
from market.in_memory_runtime_metrics_repository import (
    InMemoryRuntimeMetricsRepository
)


class DummyScheduler:

    def run_once(self, symbols):
        pass


def test_runtime_persists_metrics():

    metrics_repo = InMemoryRuntimeMetricsRepository()

    runtime = MarketDataRuntime(
        scheduler=DummyScheduler(),
        metrics_repository=metrics_repo
    )

    runtime.start()

    runtime.run_loop(
        ["BTCUSDT"],
        2
    )

    saved = metrics_repo.load_metrics()

    assert saved["successful_cycles"] == 2
    assert saved["failed_cycles"] == 0



def test_runtime_restores_metrics():

    metrics_repo = InMemoryRuntimeMetricsRepository()

    metrics_repo.save_metrics(
        {
            "successful_cycles": 10,
            "failed_cycles": 3
        }
    )

    runtime = MarketDataRuntime(
        scheduler=DummyScheduler(),
        metrics_repository=metrics_repo
    )

    metrics = runtime.metrics()

    assert metrics["successful_cycles"] == 10
    assert metrics["failed_cycles"] == 3
