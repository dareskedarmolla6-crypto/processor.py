from brain.execution_engine import ExecutionEngine
from brain.performance_memory import PerformanceMemory
from brain.execution_feedback_bridge import ExecutionFeedbackBridge


def test_execution_feedback_records_win():

    engine = ExecutionEngine()

    memory = PerformanceMemory()

    bridge = ExecutionFeedbackBridge(
        memory
    )

    position = engine.open(
        symbol="BTCUSDT",
        side="LONG",
        size=1,
        price=60000
    )

    result = engine.close_by_id(
        symbol="BTCUSDT",
        pos_id=position["id"],
        price=60100
    )

    feedback = bridge.process(
        result
    )

    assert feedback["symbol"] == "BTCUSDT"
    assert feedback["status"] == "WIN"

    assert memory.history["BTCUSDT"]["wins"] == 1



def test_execution_feedback_rejects_invalid():

    memory = PerformanceMemory()

    bridge = ExecutionFeedbackBridge(
        memory
    )

    result = bridge.process(
        {}
    )

    assert result == "INVALID_EXECUTION_RESULT"
