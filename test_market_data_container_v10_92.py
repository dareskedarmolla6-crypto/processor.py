from market.market_data_container import MarketDataContainer


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_container_creates_application():

    container = MarketDataContainer(
        StubScheduler()
    )

    assert container.application is not None


def test_container_application_can_start():

    container = MarketDataContainer(
        StubScheduler()
    )

    container.application.start()

    state = container.application.state()

    assert state["status"] == "RUNNING"


def test_container_application_can_stop():

    container = MarketDataContainer(
        StubScheduler()
    )

    container.application.start()
    container.application.stop()

    state = container.application.state()

    assert state["status"] == "STOPPED"
