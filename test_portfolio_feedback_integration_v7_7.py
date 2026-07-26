from brain.portfolio_memory import PortfolioMemory
from brain.portfolio_feedback import PortfolioFeedback


def run_test():

    print("========== PORTFOLIO FEEDBACK INTEGRATION V7.7 ==========")


    # -------------------------
    # Portfolio Memory
    # -------------------------

    memory = PortfolioMemory()


    portfolio = [
        {
            "symbol": "BTCUSDT",
            "allocation": 450,
            "action": "INCREASE"
        },
        {
            "symbol": "SOLUSDT",
            "allocation": 450,
            "action": "INCREASE"
        },
        {
            "symbol": "ETHUSDT",
            "allocation": 50,
            "action": "REDUCE"
        }
    ]


    memory.update(portfolio)


    print("\nMEMORY:")
    print(memory.get())


    # -------------------------
    # Portfolio Feedback
    # -------------------------

    feedback = PortfolioFeedback(memory)

    result = feedback.analyze()


    print("\nFEEDBACK:")
    print(result)


    # -------------------------
    # Validation
    # -------------------------

    assert result["BTCUSDT"]["decision"] == "BOOST"
    assert result["SOLUSDT"]["decision"] == "BOOST"
    assert result["ETHUSDT"]["decision"] == "PENALIZE"


    print("\nPORTFOLIO FEEDBACK INTEGRATION V7.7 PASSED ✅")


if __name__ == "__main__":
    run_test()
