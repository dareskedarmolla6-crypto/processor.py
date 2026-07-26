from market.runtime_supervisor_metrics import (
    RuntimeSupervisorMetrics
)

from market.sqlite_runtime_supervisor_metrics_repository import (
    SQLiteRuntimeSupervisorMetricsRepository
)


def test_metrics_persist_and_restore():

    repository = (
        SQLiteRuntimeSupervisorMetricsRepository(
            ":memory:"
        )
    )

    metrics = RuntimeSupervisorMetrics(
        repository=repository
    )

    metrics.increment(
        "starts"
    )

    metrics.increment(
        "recoveries"
    )


    saved = repository.load_metrics()


    assert saved == {
        "starts": 1,
        "stops": 0,
        "restarts": 0,
        "recoveries": 1,
        "recovery_failures": 0
    }



def test_metrics_update_persists():

    repository = (
        SQLiteRuntimeSupervisorMetricsRepository(
            ":memory:"
        )
    )


    metrics = RuntimeSupervisorMetrics(
        repository=repository
    )


    metrics.increment(
        "starts"
    )

    metrics.increment(
        "starts"
    )


    saved = repository.load_metrics()


    assert saved["starts"] == 2
