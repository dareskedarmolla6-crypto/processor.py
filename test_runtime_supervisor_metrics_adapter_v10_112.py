from market.runtime_supervisor_metrics import (
    RuntimeSupervisorMetrics
)

from market.runtime_supervisor_metrics_adapter import (
    RuntimeSupervisorMetricsAdapter
)


def test_adapter_records_lifecycle_metrics():

    metrics = RuntimeSupervisorMetrics()

    adapter = RuntimeSupervisorMetricsAdapter(
        metrics
    )

    adapter.record_start()
    adapter.record_stop()
    adapter.record_restart()

    adapter.record_recovery()
    adapter.record_recovery_failure()

    result = adapter.snapshot()

    assert result == {
        "starts": 1,
        "stops": 1,
        "restarts": 1,
        "recoveries": 1,
        "recovery_failures": 1
    }
