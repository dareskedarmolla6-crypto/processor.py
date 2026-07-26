from brain.self_optimizer_v10_26 import SelfOptimizerV10_26


def run_test():

    print(
        "========== SELF OPTIMIZER V10.26 =========="
    )


    optimizer = SelfOptimizerV10_26()


    performance = {
        "performance_score": 100
    }


    result = optimizer.optimize(
        performance
    )


    print("\nOPTIMIZED:")
    print(result)


    assert result["mode"] == "AGGRESSIVE"
    assert result["adjustments"] == 1


    print(
        "\nSELF OPTIMIZER V10.26 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
