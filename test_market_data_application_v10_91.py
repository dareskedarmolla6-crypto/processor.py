from market.market_data_application import MarketDataApplication


class StubOrchestrator:

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


def test_application_start():

    orchestrator = StubOrchestrator()

    app = MarketDataApplication(
        orchestrator
    )

    app.start()

    assert orchestrator.started is True


def test_application_stop():

    orchestrator = StubOrchestrator()

    app = MarketDataApplication(
        orchestrator
    )

    app.stop()

    assert orchestrator.stopped is True


def test_application_delegates():

    orchestrator = StubOrchestrator()

    app = MarketDataApplication(
        orchestrator
    )

    assert app.state()["status"] == "RUNNING"
    assert app.health()["healthy"] is True
