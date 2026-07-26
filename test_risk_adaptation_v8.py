from brain.risk_adapter import RiskAdapter


def run_test():

    print("========== RISK ADAPTATION V8.0 ==========")


    adapter = RiskAdapter()


    # WIN correction
    win = {
        "risk_adjustment": 0.02,
        "action": "IMPROVE"
    }


    win_result = adapter.apply_correction(
        win
    )


    print("\nWIN:")
    print(win_result)


    # LOSS correction
    loss = {
        "risk_adjustment": -0.02,
        "action": "PROTECT"
    }


    loss_result = adapter.apply_correction(
        loss
    )


    print("\nLOSS:")
    print(loss_result)


    assert win_result["current_risk"] > 0.03
    assert loss_result["current_risk"] < 0.05


    print("\nRISK ADAPTATION V8.0 PASSED ✅")


if __name__ == "__main__":
    run_test()
