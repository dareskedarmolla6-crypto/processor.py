from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)


class FakeRuntime:

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
            "cycles": 0,
            "last_error": None
        }


    @property
    def running(self):
        return self._running



class InMemoryMetricsRepository:

    def __init__(self):
        self._metrics = {}


    def save_metrics(
        self,
        metrics
    ):
        self._metrics = metrics.copy()


    def load_metrics(self):
        return self._metrics.copy()



def test_supervisor_initial_metrics():

    runtime = FakeRuntime()

    repository = InMemoryMetricsRepository()

    supervisor = MarketDataRuntimeSupervisor(
        runtime,
        metrics_repository=repository
    )

    metrics = repository.load_metrics()

    assert metrics == {
        "starts": 0,
        "stops": 0,
        "restarts": 0,
        "recoveries": 0,
        "recovery_failures": 0
    }



def test_supervisor_records_start_metric():

    runtime = FakeRuntime()

    repository = InMemoryMetricsRepository()

    supervisor = MarketDataRuntimeSupervisor(
        runtime,
        metrics_repository=repository
    )

    supervisor.start()

    metrics = repository.load_metrics()

    assert metrics["starts"] == 1
