from brain.performance_memory import PerformanceMemory
from brain.self_optimizer import SelfOptimizer


def run_test():

    print("========== SELF OPTIMIZER TEST ==========")


    memory = PerformanceMemory()


    # Strong symbol
    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        50
    )


    # Weak symbol
    memory.record(
        "ETHUSDT",
        -50
    )

    memory.record(
        "ETHUSDT",
        -20
    )


    optimizer = SelfOptimizer(
        memory
    )


    report = optimizer.analyze()

    print("\nANALYSIS:")
    print(report)



    result = optimizer.optimize()


    print("\nOPTIMIZATION:")
    print(result)



    assert report["BTCUSDT"]["status"] == "STRONG"
    assert report["ETHUSDT"]["status"] == "WEAK"


    print(
        "\nSELF OPTIMIZER TEST PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
