from brain.portfolio_intelligence import PortfolioIntelligence


def run_test():

    print("========== PORTFOLIO INTELLIGENCE V9.2 ==========")

    brain = PortfolioIntelligence(max_positions=2)

    decisions = [
        {"symbol": "BTCUSDT", "confidence": 0.95, "decision": "TRADE"},
        {"symbol": "ETHUSDT", "confidence": 0.91, "decision": "TRADE"},
        {"symbol": "BNBUSDT", "confidence": 0.72, "decision": "TRADE"},
        {"symbol": "XRPUSDT", "confidence": 0.55, "decision": "SKIP"},
    ]

    selected = brain.select(decisions)

    print("\nSELECTED:")
    print(selected)

    stats = brain.statistics(decisions)

    print("\nSTATISTICS:")
    print(stats)

    assert len(selected) == 2
    assert selected[0]["symbol"] == "BTCUSDT"
    assert selected[1]["symbol"] == "ETHUSDT"

    print("\nPORTFOLIO INTELLIGENCE V9.2 PASSED ✅")


if __name__ == "__main__":
    run_test()
