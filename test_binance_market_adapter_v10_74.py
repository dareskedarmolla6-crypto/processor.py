from market.binance_market_adapter import BinanceMarketAdapter


def test_from_ticker():

    adapter = BinanceMarketAdapter()

    ticker = {
        "symbol": "BTCUSDT",
        "price": "60000.00"
    }

    state = adapter.from_ticker(
        ticker
    )

    assert state.symbol == "BTCUSDT"
    assert state.exchange == "BINANCE"
    assert state.last_price == 60000.0


def test_from_24h():

    adapter = BinanceMarketAdapter()

    ticker = {
        "symbol": "BTCUSDT",
        "lastPrice": "60000.00",
        "bidPrice": "59999.00",
        "askPrice": "60001.00",
        "volume": "2500.00"
    }

    state = adapter.from_24h(
        ticker
    )

    assert state.symbol == "BTCUSDT"
    assert state.exchange == "BINANCE"
    assert state.last_price == 60000.0
    assert state.bid_price == 59999.0
    assert state.ask_price == 60001.0
    assert state.volume == 2500.0
    assert state.market_status == "ACTIVE"


if __name__ == "__main__":

    test_from_ticker()
    test_from_24h()

    print(
        "BinanceMarketAdapter Tests PASSED ✅"
    )
