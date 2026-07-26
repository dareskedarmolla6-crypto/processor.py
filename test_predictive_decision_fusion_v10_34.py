from brain.predictive_decision_fusion_v10_34 import (
    PredictiveDecisionFusionV10_34
)

from brain.autonomous_knowledge_core_v10_31 import (
    AutonomousKnowledgeCoreV10_31
)

from brain.adaptive_brain_v10_27 import (
    AdaptiveBrainV10_27
)



def run_test():

    print(
        "========== PREDICTIVE DECISION FUSION V10.34 =========="
    )


    knowledge = AutonomousKnowledgeCoreV10_31()


    knowledge.remember(
        "BTCUSDT",
        "STRONG_BUY_PATTERN",
        "WIN"
    )


    brain = AdaptiveBrainV10_27()


    fusion = PredictiveDecisionFusionV10_34(
        knowledge,
        brain
    )


    decision = fusion.decide(
        {
            "symbol":"BTCUSDT",
            "signal":"BUY",
            "confidence":0.90
        }
    )


    print("\nDECISION:")
    print(decision)


    print("\nSTATE:")
    print(
        fusion.state()
    )


    assert decision["decision"] == "TRADE"
    assert decision["prediction"]["patterns_found"] == 1


    print(
        "\nPREDICTIVE DECISION FUSION V10.34 PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
