from brain.performance_memory import PerformanceMemory
from brain.portfolio_memory import PortfolioMemory
from brain.portfolio_feedback import PortfolioFeedback
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    print("========== ADAPTIVE BRAIN FEEDBACK V7.8 ==========")


    # -------------------------
    # Performance Memory
    # -------------------------

    memory = PerformanceMemory()

    memory.record("BTCUSDT", 100)
    memory.record("ETHUSDT", -80)


    # -------------------------
    # Portfolio Memory
    # -------------------------

    portfolio_memory = PortfolioMemory()

    portfolio_memory.update([
        {
            "symbol": "BTCUSDT",
            "allocation": 450,
            "action": "INCREASE"
        },
        {
            "symbol": "ETHUSDT",
            "allocation": 50,
            "action": "REDUCE"
        }
    ])


    # -------------------------
    # Portfolio Feedback
    # -------------------------

    portfolio_feedback = PortfolioFeedback(
        portfolio_memory
    )

    feedback = portfolio_feedback.analyze()

    print("\nFEEDBACK:")
    print(feedback)


    # -------------------------
    # Brain
    # -------------------------

    brain = AdaptiveBrain(memory)

    brain.inject_feedback(
        feedback
    )


    btc = brain.evaluate(
        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.90
        }
    )


    eth = brain.evaluate(
        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "confidence": 0.80
        }
    )


    print("\nBTC:")
    print(btc)

    print("\nETH:")
    print(eth)


    assert btc["confidence"] > 0.90
    assert eth["confidence"] < 0.80


    print("\nADAPTIVE BRAIN FEEDBACK V7.8 PASSED ✅")


if __name__ == "__main__":
    run_test()
