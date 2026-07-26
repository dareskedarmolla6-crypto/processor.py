from market.runtime_supervisor_metrics import (
    RuntimeSupervisorMetrics
)

from market.runtime_supervisor_metrics_adapter import (
    RuntimeSupervisorMetricsAdapter
)


class FakeRuntime:

    def __init__(self):
        self._running = False
        self._healthy = True


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
            "healthy": self._healthy,
            "cycles": 0,
            "last_error": None
        }


    @property
    def running(self):
        return self._running



def test_supervisor_metrics_adapter_flow():

    runtime = FakeRuntime()

    metrics = RuntimeSupervisorMetrics()

    adapter = RuntimeSupervisorMetricsAdapter(
        metrics
    )


    runtime.start()
    adapter.record_start()


    runtime.stop()
    adapter.record_stop()


    runtime.restart()
    adapter.record_restart()


    adapter.record_recovery()


    result = adapter.snapshot()


    assert result == {
        "starts": 1,
        "stops": 1,
        "restarts": 1,
        "recoveries": 1,
        "recovery_failures": 0
    }
