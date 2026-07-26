from brain.memory_manager import MemoryManager
from brain.autonomous_brain import AutonomousBrain
from brain.self_optimizer import SelfOptimizer


def run_test():

    print("========== BRAIN RESTART RECOVERY TEST ==========")


    db = "restart_test.db"


    # =====================
    # FIRST SESSION
    # =====================

    memory = MemoryManager(
        db
    )


    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        50
    )

    memory.record(
        "ETHUSDT",
        -50
    )


    print("\nBEFORE RESTART:")
    print(memory.history)


    memory.close()



    # =====================
    # RESTART SIMULATION
    # =====================

    memory2 = MemoryManager(
        db
    )


    print("\nAFTER RESTART:")
    print(memory2.history)



    # =====================
    # BRAIN RECOVERY
    # =====================

    brain = AutonomousBrain(
        memory2.live_memory
    )


    signals = [

        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "price": 60000,
            "confidence": 0.75
        },

        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "price": 3000,
            "confidence": 0.75
        }

    ]


    result = brain.run_cycle(
        signals
    )


    print("\nRECOVERED BRAIN:")
    print(result)



    btc = next(
        x for x in result["decisions"]
        if x["symbol"] == "BTCUSDT"
    )


    eth = next(
        x for x in result["decisions"]
        if x["symbol"] == "ETHUSDT"
    )


    assert btc["confidence"] > 0.75

    assert eth["confidence"] < 0.75


    memory2.close()


    print(
        "\nBRAIN RESTART RECOVERY TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
