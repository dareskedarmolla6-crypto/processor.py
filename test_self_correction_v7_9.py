from brain.self_correction import SelfCorrection


def run_test():

    print("========== SELF CORRECTION V7.9 ==========")


    correction = SelfCorrection()


    # -------------------------
    # WIN SCENARIO
    # -------------------------

    win_feedback = [
        {
            "symbol": "BTCUSDT",
            "pnl": 100
        },
        {
            "symbol": "SOLUSDT",
            "pnl": 150
        }
    ]


    win_result = correction.analyze(
        win_feedback
    )


    print("\nWIN CORRECTION:")
    print(win_result)


    # -------------------------
    # LOSS SCENARIO
    # -------------------------

    loss_feedback = [
        {
            "symbol": "ETHUSDT",
            "pnl": -80
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -50
        }
    ]


    loss_result = correction.analyze(
        loss_feedback
    )


    print("\nLOSS CORRECTION:")
    print(loss_result)


    # -------------------------
    # VALIDATION
    # -------------------------

    assert win_result["action"] == "IMPROVE"
    assert win_result["confidence_adjustment"] > 0

    assert loss_result["action"] == "PROTECT"
    assert loss_result["risk_adjustment"] < 0


    print("\nSELF CORRECTION V7.9 PASSED ✅")


if __name__ == "__main__":
    run_test()
