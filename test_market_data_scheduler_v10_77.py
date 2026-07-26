from market.market_data_scheduler import MarketDataScheduler


class StubService:

    def __init__(self):
        self.calls = []

    def update(self, symbols):
        self.calls.append(symbols)


def test_scheduler_runs_service_update():

    service = StubService()

    scheduler = MarketDataScheduler(
        service
    )

    scheduler.run_once(
        [
            "BTCUSDT",
            "ETHUSDT"
        ]
    )

    assert service.calls == [
        [
            "BTCUSDT",
            "ETHUSDT"
        ]
    ]


def test_scheduler_rejects_empty_symbols():

    service = StubService()

    scheduler = MarketDataScheduler(
        service
    )

    try:
        scheduler.run_once([])

        assert False

    except ValueError:
        assert True


if __name__ == "__main__":

    test_scheduler_runs_service_update()
    test_scheduler_rejects_empty_symbols()

    print(
        "MarketDataScheduler Tests PASSED ✅"
    )
