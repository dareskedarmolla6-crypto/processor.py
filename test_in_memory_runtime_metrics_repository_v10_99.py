from market.in_memory_runtime_metrics_repository import (
    InMemoryRuntimeMetricsRepository
)


def test_save_and_load_metrics():

    repo = InMemoryRuntimeMetricsRepository()

    metrics = {
        "successful_cycles": 10,
        "failed_cycles": 2
    }

    repo.save_metrics(metrics)

    restored = repo.load_metrics()

    assert restored == metrics


def test_metrics_snapshot_is_copy():

    repo = InMemoryRuntimeMetricsRepository()

    repo.save_metrics(
        {
            "successful_cycles": 5,
            "failed_cycles": 1
        }
    )

    metrics = repo.load_metrics()

    metrics["successful_cycles"] = 999

    assert repo.load_metrics()[
        "successful_cycles"
    ] == 5
