from market.market_data_coordinator import MarketDataCoordinator
from models.symbol_state import SymbolState


class StubMarketClient:

    def get_ticker_24h(self, symbol):

        return {
            "symbol": symbol,
            "lastPrice": "60000.0",
            "bidPrice": "59999.0",
            "askPrice": "60001.0",
            "volume": "2500.0"
        }


class StubAdapter:

    def from_24h(self, ticker):

        return SymbolState(
            symbol=ticker["symbol"],
            exchange="BINANCE",
            last_price=float(ticker["lastPrice"]),
            bid_price=float(ticker["bidPrice"]),
            ask_price=float(ticker["askPrice"]),
            volume=float(ticker["volume"]),
            market_status="ACTIVE"
        )


class StubManager:

    def __init__(self):
        self.state = None

    def load_validated_symbol(self, state):
        self.state = state


def test_market_data_coordinator():

    client = StubMarketClient()
    adapter = StubAdapter()
    manager = StubManager()

    coordinator = MarketDataCoordinator(
        client,
        adapter,
        manager
    )

    coordinator.update_symbol(
        "BTCUSDT"
    )

    assert manager.state is not None
    assert manager.state.symbol == "BTCUSDT"
    assert manager.state.last_price == 60000.0


if __name__ == "__main__":

    test_market_data_coordinator()

    print(
        "MarketDataCoordinator Tests PASSED ✅"
    )
