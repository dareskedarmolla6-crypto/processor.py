from brain.experience_learning_engine_v10_36 import (
    ExperienceLearningEngineV10_36
)


def run_test():

    print(
        "========== EXPERIENCE LEARNING ENGINE V10.36 =========="
    )


    engine = ExperienceLearningEngineV10_36()


    memory_record = {

        "symbol":
            "BTCUSDT",

        "decision":
            "TRADE",

        "confidence":
            0.85,

        "result":
            "WIN"
    }


    result = engine.learn(
        memory_record
    )


    print("\nLEARNING:")
    print(result)


    knowledge = engine.knowledge_update()


    print("\nKNOWLEDGE UPDATE:")
    print(knowledge)


    print("\nSTATE:")
    print(engine.state())


    assert result["status"] == "LEARNED"
    assert knowledge["strong_patterns"] == 1
    assert knowledge["weak_patterns"] == 0


    print(
        "\nEXPERIENCE LEARNING ENGINE V10.36 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
