from market.runtime_supervisor_metrics import (
    RuntimeSupervisorMetrics
)


class InMemoryMetricsRepository:
    """
    Test persistence repository.
    """

    def __init__(self):
        self.data = {}


    def save_metrics(
        self,
        metrics: dict
    ):
        self.data = metrics.copy()


    def load_metrics(self):
        return self.data.copy()



def test_health_metrics_initial_state():

    metrics = RuntimeSupervisorMetrics()

    snapshot = metrics.snapshot()

    assert snapshot == {
        "starts": 0,
        "stops": 0,
        "restarts": 0,
        "recoveries": 0,
        "recovery_failures": 0,
        "health_checks": 0,
        "healthy_states": 0,
        "degraded_states": 0,
        "failed_states": 0
    }



def test_health_state_recording():

    metrics = RuntimeSupervisorMetrics()


    metrics.record_health_state(
        "healthy"
    )

    metrics.record_health_state(
        "degraded"
    )

    metrics.record_health_state(
        "failed"
    )


    snapshot = metrics.snapshot()


    assert snapshot["health_checks"] == 3

    assert snapshot["healthy_states"] == 1

    assert snapshot["degraded_states"] == 1

    assert snapshot["failed_states"] == 1



def test_health_metrics_persistence():

    repository = InMemoryMetricsRepository()


    metrics = RuntimeSupervisorMetrics(
        repository=repository
    )


    metrics.record_health_state(
        "healthy"
    )

    metrics.record_health_state(
        "failed"
    )


    restored = RuntimeSupervisorMetrics(
        repository=repository
    )


    snapshot = restored.snapshot()


    assert snapshot["health_checks"] == 2

    assert snapshot["healthy_states"] == 1

    assert snapshot["failed_states"] == 1



def test_invalid_health_state_rejected():

    metrics = RuntimeSupervisorMetrics()


    try:

        metrics.record_health_state(
            "unknown"
        )

        assert False


    except ValueError:

        assert True
