from brain.self_optimizer_v10_6 import SelfOptimizerV10_6


def run_test():

    print(
        "========== SELF OPTIMIZER V10.6 =========="
    )


    optimizer = SelfOptimizerV10_6()


    learning = {

        "mode": "AGGRESSIVE"

    }


    state = optimizer.optimize(
        learning
    )


    print("\nOPTIMIZED STATE:")
    print(state)


    decision = {

        "symbol": "BTCUSDT",

        "confidence": 0.85

    }


    result = optimizer.apply(
        decision
    )


    print("\nDECISION:")
    print(result)


    assert state["mode"] == "AGGRESSIVE"

    assert state["risk_level"] == 0.04

    assert result["optimizer_mode"] == "AGGRESSIVE"


    print(
        "\nSELF OPTIMIZER V10.6 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
