from brain.long_term_memory_v10_18 import LongTermMemoryV10_18


def run_test():

    print(
        "========== LONG TERM MEMORY V10.18 =========="
    )


    memory = LongTermMemoryV10_18(
        "test_memory.json"
    )


    result = memory.remember(
        "BTCUSDT",
        {
            "pnl":100,
            "result":"WIN"
        }
    )


    print("\nSAVE RESULT:")
    print(result)


    # simulate restart

    recovered = LongTermMemoryV10_18(
        "test_memory.json"
    )


    state = recovered.get_memory()


    print("\nRECOVERED:")
    print(state)


    assert (
        state["history"]["BTCUSDT"][0]["pnl"]
        == 100
    )


    print(
        "\nLONG TERM MEMORY V10.18 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
