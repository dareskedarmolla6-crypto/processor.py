from brain.portfolio_allocator_v9_4 import PortfolioAllocatorV9_4


def run_test():

    print("========== PORTFOLIO ALLOCATOR V9.4 ==========")


    allocator = PortfolioAllocatorV9_4(
        total_capital=1000
    )


    decisions = [

        {
            "symbol": "BTCUSDT",
            "confidence": 1.0,
            "decision": "TRADE",
            "risk_level": 0.05
        },

        {
            "symbol": "ETHUSDT",
            "confidence": 0.8,
            "decision": "TRADE",
            "risk_level": 0.04
        },

        {
            "symbol": "BNBUSDT",
            "confidence": 0.2,
            "decision": "SKIP",
            "risk_level": 0.03
        }

    ]


    result = allocator.allocate(
        decisions
    )


    print("\nALLOCATIONS:")
    print(result)


    assert len(result) == 2

    assert result[0]["symbol"] == "BTCUSDT"

    assert result[0]["allocation"] > result[1]["allocation"]


    print(
        "\nPORTFOLIO ALLOCATOR V9.4 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
