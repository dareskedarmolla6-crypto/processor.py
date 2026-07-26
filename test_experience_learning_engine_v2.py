from brain.experience_learning_engine_v2 import (
    ExperienceLearningEngineV2
)


def test_learning_win_pattern():

    engine = ExperienceLearningEngineV2()

    result = engine.learn(
        {
            "symbol": "BTCUSDT",
            "decision": "BUY",
            "confidence": 0.85,
            "result": "WIN"
        }
    )

    assert result["status"] == "LEARNED"

    state = engine.state()

    assert state["experiences"] == 1
    assert state["patterns"]["strong"] == 1



def test_learning_loss_pattern():

    engine = ExperienceLearningEngineV2()

    engine.learn(
        {
            "symbol": "ETHUSDT",
            "decision": "SELL",
            "confidence": 0.60,
            "result": "LOSS"
        }
    )

    knowledge = engine.knowledge_update()

    assert knowledge["weak_patterns"] == 1



def test_learning_history_copy():

    engine = ExperienceLearningEngineV2()

    engine.learn(
        {
            "symbol": "BTCUSDT",
            "decision": "BUY",
            "confidence": 0.90,
            "result": "WIN"
        }
    )

    history = engine.history()

    history[0]["result"] = "LOSS"

    assert engine.history()[0]["result"] == "WIN"
