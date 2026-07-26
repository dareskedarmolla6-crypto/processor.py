from brain.performance_memory import PerformanceMemory
from brain.feedback_engine import FeedbackEngine


def run_feedback_test():

    print("========== FEEDBACK LEARNING TEST ==========")


    memory = PerformanceMemory()


    feedback = FeedbackEngine(
        memory
    )


    # =====================
    # SINGLE RESULTS
    # =====================

    btc = feedback.process_result(
        "BTCUSDT",
        100
    )


    eth = feedback.process_result(
        "ETHUSDT",
        -50
    )


    print("\nBTC RESULT:")
    print(btc)


    print("\nETH RESULT:")
    print(eth)



    # =====================
    # BATCH RESULTS
    # =====================

    batch = feedback.process_batch(
        [
            {
                "symbol": "SOLUSDT",
                "pnl": 80
            },
            {
                "symbol": "BNBUSDT",
                "pnl": -30
            }
        ]
    )


    print("\nBATCH:")
    print(batch)



    print("\nMEMORY:")
    print(memory.history)


    assert btc["status"] == "WIN"
    assert eth["status"] == "LOSS"

    assert memory.score("BTCUSDT") == 100.0
    assert memory.score("ETHUSDT") == 0.0


    print(
        "\nFEEDBACK LEARNING TEST PASSED ✅"
    )


if __name__ == "__main__":
    run_feedback_test()
