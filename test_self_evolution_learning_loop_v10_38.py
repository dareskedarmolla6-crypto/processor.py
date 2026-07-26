from brain.self_evolution_learning_loop_v10_38 import (
    SelfEvolutionLearningLoopV10_38
)

from brain.autonomous_learning_integration_v10_37 import (
    AutonomousLearningIntegrationV10_37
)

from brain.decision_memory_replay_v10_35 import (
    DecisionMemoryReplayV10_35
)

from brain.experience_learning_engine_v10_36 import (
    ExperienceLearningEngineV10_36
)



def run_test():

    print(
        "========== SELF EVOLUTION LEARNING LOOP V10.38 =========="
    )


    memory = DecisionMemoryReplayV10_35()

    learning = ExperienceLearningEngineV10_36()


    memory.remember(
        {
            "symbol":"BTCUSDT",
            "decision":"TRADE",
            "confidence":0.85
        },
        "WIN"
    )


    integration = AutonomousLearningIntegrationV10_37(
        memory,
        learning
    )


    evolution = SelfEvolutionLearningLoopV10_38(
        integration
    )


    result = evolution.evolve(
        "BTCUSDT",
        rounds=3
    )


    print("\nEVOLUTION:")
    print(result)


    print("\nSTATE:")
    print(
        evolution.state()
    )


    assert result["status"] == "EVOLVED"
    assert result["cycles"] == 3
    assert result["growth"] == 3


    print(
        "\nSELF EVOLUTION LEARNING LOOP V10.38 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
