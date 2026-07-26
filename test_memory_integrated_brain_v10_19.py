from brain.memory_integrated_brain_v10_19 import MemoryIntegratedBrainV10_19
from brain.performance_memory import PerformanceMemory
from brain.long_term_memory_v10_18 import LongTermMemoryV10_18


def run_test():

    print(
        "========== MEMORY INTEGRATED BRAIN V10.19 =========="
    )


    long_memory = LongTermMemoryV10_18(
        "test_memory_v19.json"
    )


    long_memory.remember(
        "BTCUSDT",
        {
            "pnl":100,
            "result":"WIN"
        }
    )

    long_memory.remember(
        "BTCUSDT",
        {
            "pnl":50,
            "result":"WIN"
        }
    )


    memory = PerformanceMemory()


    brain = MemoryIntegratedBrainV10_19(
        memory,
        long_memory
    )


    decision = brain.think(
        {
            "symbol":"BTCUSDT",
            "signal":"BUY",
            "confidence":0.80
        }
    )


    print("\nDECISION:")
    print(decision)


    assert decision["confidence"] >= 0.80


    print(
        "\nMEMORY INTEGRATED BRAIN V10.19 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
