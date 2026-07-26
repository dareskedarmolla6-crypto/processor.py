from market.market_data_orchestrator import MarketDataOrchestrator


class StubSupervisor:

    def __init__(self):
        self.started = False
        self.stopped = False

    def start(self):
        self.started = True

    def stop(self):
        self.stopped = True

    def restart(self):
        return {
            "status": "RUNNING"
        }

    def state(self):
        return {
            "status": "RUNNING"
        }

    def health(self):
        return {
            "healthy": True
        }

    def metrics(self):
        return {
            "successful_cycles": 5,
            "failed_cycles": 0
        }

    def events(self):
        return [
            "runtime_started"
        ]


def test_orchestrator_start():

    supervisor = StubSupervisor()
    orchestrator = MarketDataOrchestrator(
        supervisor
    )

    orchestrator.start()

    assert supervisor.started is True


def test_orchestrator_stop():

    supervisor = StubSupervisor()
    orchestrator = MarketDataOrchestrator(
        supervisor
    )

    orchestrator.stop()

    assert supervisor.stopped is True


def test_orchestrator_delegates():

    supervisor = StubSupervisor()
    orchestrator = MarketDataOrchestrator(
        supervisor
    )

    assert orchestrator.state()["status"] == "RUNNING"
    assert orchestrator.health()["healthy"] is True
    assert orchestrator.metrics()["successful_cycles"] == 5
    assert orchestrator.events() == [
        "runtime_started"
    ]
