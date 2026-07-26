from market.market_data_service_entry import (
    MarketDataServiceEntry
)


class StubBootstrap:

    def __init__(self):
        self.called = False

    def initialize(self):
        self.called = True


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_entry_bootstrap_is_explicit():

    bootstrap = StubBootstrap()

    service = MarketDataServiceEntry(
        scheduler=StubScheduler()
    )

    service._bootstrap = bootstrap

    service.initialize()

    assert bootstrap.called is True


def test_entry_start_does_not_require_bootstrap():

    service = MarketDataServiceEntry(
        scheduler=StubScheduler()
    )

    service.start()

    state = service.state()

    assert state["status"] == "RUNNING"
