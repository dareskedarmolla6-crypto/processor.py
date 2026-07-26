from market.market_data_service_entry import (
    MarketDataServiceEntry
)


class StubScheduler:

    def run_once(self, symbols):
        pass


def test_service_entry_start():

    service = MarketDataServiceEntry(
        StubScheduler()
    )

    service.start()

    state = service.state()

    assert state["status"] == "RUNNING"


def test_service_entry_stop():

    service = MarketDataServiceEntry(
        StubScheduler()
    )

    service.start()
    service.stop()

    state = service.state()

    assert state["status"] == "STOPPED"


def test_service_entry_state_exposure():

    service = MarketDataServiceEntry(
        StubScheduler()
    )

    state = service.state()

    assert "status" in state
