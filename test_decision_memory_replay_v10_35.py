from brain.decision_memory_replay_v10_35 import (
    DecisionMemoryReplayV10_35
)


def run_test():

    print(
        "========== DECISION MEMORY REPLAY V10.35 =========="
    )


    memory = DecisionMemoryReplayV10_35()


    decision = {

        "symbol":
            "BTCUSDT",

        "decision":
            "TRADE",

        "confidence":
            0.85
    }


    saved = memory.remember(
        decision,
        "WIN"
    )


    print("\nSAVED:")
    print(saved)


    replay = memory.replay(
        "BTCUSDT"
    )


    print("\nREPLAY:")
    print(replay)


    analysis = memory.analyze()


    print("\nANALYSIS:")
    print(analysis)


    print("\nSTATE:")
    print(memory.state())


    assert saved["status"] == "REMEMBERED"
    assert len(replay) == 1
    assert analysis["performance_score"] == 100.0


    print(
        "\nDECISION MEMORY REPLAY V10.35 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
