from clients.binance_client import BinanceClient
from clients.binance_market_data_client import BinanceMarketDataClient
from market.real_market_feed_adapter import RealMarketFeedAdapter


def main():

    print(
        "========== REAL MARKET FEED TEST V10.52 =========="
    )


    client = BinanceClient()

    market_client = BinanceMarketDataClient(
        client
    )


    adapter = RealMarketFeedAdapter(
        market_client,
        [
            "BTCUSDT"
        ]
    )


    snapshot = adapter.fetch()


    print(
        snapshot
    )


    assert snapshot
    assert snapshot[0]["symbol"] == "BTCUSDT"
    assert snapshot[0]["price"] > 0


    print(
        "✅ REAL MARKET FEED TEST PASSED"
    )


if __name__ == "__main__":
    main()
