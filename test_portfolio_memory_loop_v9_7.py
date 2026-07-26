from brain.portfolio_memory_loop_v9_7 import PortfolioMemoryLoopV9_7


def run_test():

    print("========== PORTFOLIO MEMORY LOOP V9.7 ==========")


    memory = PortfolioMemoryLoopV9_7()


    memory.record_trade(
        "BTCUSDT",
        100
    )


    memory.record_trade(
        "ETHUSDT",
        -50
    )


    btc = memory.analyze(
        "BTCUSDT"
    )

    eth = memory.analyze(
        "ETHUSDT"
    )


    print("\nBTC:")
    print(btc)


    print("\nETH:")
    print(eth)


    memory.record_cycle(
        {
            "status":"LEARNED"
        }
    )


    print("\nMEMORY:")
    print(
        memory.get_memory()
    )


    assert btc["rating"] == "STRONG"

    assert eth["rating"] == "WEAK"

    assert len(
        memory.get_memory()["history"]
    ) == 1


    print(
        "\nPORTFOLIO MEMORY LOOP V9.7 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
