from market.market_data_service import MarketDataService


class StubCoordinator:

    def __init__(self):
        self.updated = []

    def update_symbol(self, symbol):
        self.updated.append(symbol)


def test_market_data_service_updates_all_symbols():

    coordinator = StubCoordinator()

    service = MarketDataService(
        coordinator
    )

    service.update(
        [
            "BTCUSDT",
            "ETHUSDT",
            "BNBUSDT"
        ]
    )

    assert coordinator.updated == [
        "BTCUSDT",
        "ETHUSDT",
        "BNBUSDT"
    ]


def test_market_data_service_rejects_empty_symbols():

    coordinator = StubCoordinator()

    service = MarketDataService(
        coordinator
    )

    try:
        service.update([])
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":

    test_market_data_service_updates_all_symbols()
    test_market_data_service_rejects_empty_symbols()

    print(
        "MarketDataService Tests PASSED ✅"
    )
