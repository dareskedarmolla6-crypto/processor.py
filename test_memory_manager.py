from brain.memory_manager import MemoryManager


def run_test():

    print("========== MEMORY MANAGER TEST ==========")


    db = "manager_test.db"


    # -------------------------
    # First Session
    # -------------------------

    memory = MemoryManager(
        db
    )


    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        -20
    )

    memory.record(
        "ETHUSDT",
        50
    )


    print("\nSESSION 1:")
    print(memory.history)


    memory.close()



    # -------------------------
    # Restart Simulation
    # -------------------------

    memory2 = MemoryManager(
        db
    )


    print("\nSESSION 2 AFTER RELOAD:")
    print(memory2.history)



    assert (
        memory2.history["BTCUSDT"]["trades"]
        == 2
    )


    assert (
        memory2.history["BTCUSDT"]["pnl"]
        == 80
    )


    assert (
        memory2.history["ETHUSDT"]["pnl"]
        == 50
    )


    memory2.close()


    print(
        "\nMEMORY MANAGER TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
