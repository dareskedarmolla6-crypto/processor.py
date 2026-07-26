from market.market_data_supervisor import MarketDataSupervisor


class StubRuntime:

    def __init__(self):
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def restart(self):
        return {"status": "RUNNING"}

    def state(self):
        return {"status": "RUNNING"}

    def health(self):
        return {"healthy": True}

    def metrics(self):
        return {
            "successful_cycles": 3,
            "failed_cycles": 1
        }

    def events(self):
        return [
            "runtime_started"
        ]


def test_supervisor_start():
    runtime = StubRuntime()
    supervisor = MarketDataSupervisor(runtime)

    supervisor.start()

    assert runtime.started is True


def test_supervisor_stop():
    runtime = StubRuntime()
    supervisor = MarketDataSupervisor(runtime)

    supervisor.stop()

    assert runtime.stopped is True


def test_supervisor_delegates_runtime_information():
    runtime = StubRuntime()
    supervisor = MarketDataSupervisor(runtime)

    assert supervisor.state()["status"] == "RUNNING"
    assert supervisor.health()["healthy"] is True
    assert supervisor.metrics()["successful_cycles"] == 3
    assert supervisor.events() == ["runtime_started"]
