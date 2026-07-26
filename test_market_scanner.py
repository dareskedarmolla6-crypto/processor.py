from brain.market_scanner import MarketScanner


def run_market_scanner_test():

    print("========== MARKET SCANNER TEST ==========")

    scanner = MarketScanner(min_confidence=0.75)

    market = [
        {
            "symbol": "BTCUSDT",
            "price": 60000,
            "signal": "BUY",
            "confidence": 0.95
        },
        {
            "symbol": "ETHUSDT",
            "price": 3000,
            "signal": "BUY",
            "confidence": 0.82
        },
        {
            "symbol": "SOLUSDT",
            "price": 150,
            "signal": "SELL",
            "confidence": 0.60
        },
        {
            "symbol": "BNBUSDT",
            "price": 700,
            "signal": "BUY",
            "confidence": 0.88
        }
    ]

    result = scanner.scan(market)

    print("\nFILTERED OPPORTUNITIES:")
    for item in result:
        print(item)

    assert len(result) == 3

    print("\nMARKET SCANNER TEST PASSED ✅")


if __name__ == "__main__":
    run_market_scanner_test()
