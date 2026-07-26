from brain.persistent_memory import PersistentMemory


def run_test():

    print("========== PERSISTENT MEMORY TEST ==========")


    memory = PersistentMemory(
        "test_memory.db"
    )


    # -------------------------
    # SAVE TRADES
    # -------------------------

    memory.save_trade(
        "BTCUSDT",
        100
    )

    memory.save_trade(
        "BTCUSDT",
        -20
    )

    memory.save_trade(
        "ETHUSDT",
        50
    )


    # -------------------------
    # LOAD HISTORY
    # -------------------------

    history = memory.load_history()


    print("\nHISTORY:")
    print(history)



    assert history["BTCUSDT"]["trades"] == 2

    assert history["BTCUSDT"]["wins"] == 1

    assert history["BTCUSDT"]["losses"] == 1

    assert history["ETHUSDT"]["pnl"] == 50



    memory.close()


    print(
        "\nPERSISTENT MEMORY TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
