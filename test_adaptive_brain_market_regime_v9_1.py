from brain.performance_memory import PerformanceMemory
from brain.adaptive_brain import AdaptiveBrain
from brain.market_regime import MarketRegime


def run_test():

    print("========== ADAPTIVE BRAIN MARKET REGIME V9.1 ==========")

    # -------------------------
    # Performance Memory
    # -------------------------

    memory = PerformanceMemory()

    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        80
    )

    # -------------------------
    # Market Regime
    # -------------------------

    regime = MarketRegime()

    regime.set_regime("TRENDING")

    # -------------------------
    # Brain
    # -------------------------

    brain = AdaptiveBrain(
        performance_memory=memory,
        market_regime=regime
    )

    brain.inject_feedback(
        {
            "BTCUSDT": {
                "adjustment": 0.05
            }
        }
    )

    signal = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "confidence": 0.90
    }

    result = brain.evaluate(signal)

    print("\nRESULT:")
    print(result)

    assert result["decision"] == "TRADE"
    assert result["market_regime"] == "TRENDING"
    assert result["confidence"] >= 0.95

    print("\nADAPTIVE BRAIN MARKET REGIME V9.1 PASSED ✅")


if __name__ == "__main__":
    run_test()
