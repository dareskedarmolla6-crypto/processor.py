from brain.execution_engine import ExecutionEngine
from brain.performance_memory import PerformanceMemory
from brain.execution_feedback_bridge import ExecutionFeedbackBridge


def test_full_autonomous_execution_learning_cycle():

    print(
        "========== FULL AUTONOMOUS EXECUTION CYCLE V10.131 =========="
    )

    memory = PerformanceMemory()

    feedback = ExecutionFeedbackBridge(
        memory
    )

    execution = ExecutionEngine()


    # OPEN
    position = execution.open(
        symbol="BTCUSDT",
        side="LONG",
        size=1,
        price=60000
    )


    assert position["status"] == "OPEN"


    # CLOSE WITH PROFIT
    closed = execution.close_by_id(
        symbol="BTCUSDT",
        pos_id=position["id"],
        price=60200
    )


    assert closed["status"] == "CLOSED"
    assert closed["realized_pnl"] == 200


    # FEEDBACK TO LEARNING MEMORY
    result = feedback.process(
        closed
    )


    print("\nFEEDBACK:")
    print(result)


    assert result["symbol"] == "BTCUSDT"
    assert result["status"] == "WIN"


    assert (
        memory.history["BTCUSDT"]["wins"]
        == 1
    )


    assert (
        memory.history["BTCUSDT"]["pnl"]
        == 200
    )


    print(
        "\nFULL AUTONOMOUS EXECUTION CYCLE PASSED ✅"
    )


if __name__ == "__main__":
    test_full_autonomous_execution_learning_cycle()
