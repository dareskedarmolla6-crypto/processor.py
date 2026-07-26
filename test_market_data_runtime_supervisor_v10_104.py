from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)


class DummyRuntime:
    def __init__(self):
        self.started = False

    def start(self):
        self.started = True

    def stop(self):
        self.started = False

    def restart(self):
        self.started = True
        return {
            "status": "RUNNING"
        }

    def health(self):
        return {
            "status": "RUNNING",
            "healthy": True
        }

    def state(self):
        return {
            "status": "RUNNING"
        }

    @property
    def running(self):
        return self.started



def test_supervisor_start_stop():

    runtime = DummyRuntime()

    supervisor = MarketDataRuntimeSupervisor(
        runtime
    )

    supervisor.start()

    assert supervisor.running is True

    supervisor.stop()

    assert supervisor.running is False



def test_supervisor_health():

    runtime = DummyRuntime()

    supervisor = MarketDataRuntimeSupervisor(
        runtime
    )

    health = supervisor.health()

    assert health["healthy"] is True



def test_supervisor_restart():

    runtime = DummyRuntime()

    supervisor = MarketDataRuntimeSupervisor(
        runtime
    )

    result = supervisor.restart()

    assert result["status"] == "RUNNING"
