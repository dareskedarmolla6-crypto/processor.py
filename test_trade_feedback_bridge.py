from brain.execution_engine import ExecutionEngine
from brain.reward_engine import RewardEngine
from brain.performance_memory import PerformanceMemory
from brain.trade_feedback_bridge import TradeFeedbackBridge


def run_test():

    execution = ExecutionEngine()

    memory = PerformanceMemory()

    reward = RewardEngine(
        memory
    )

    bridge = TradeFeedbackBridge(
        reward
    )


    position = execution.open(
        "BTCUSDT",
        "LONG",
        1,
        100
    )


    closed = execution.close_by_id(
        "BTCUSDT",
        position["id"],
        120
    )


    result = bridge.process_close(
        "BTCUSDT",
        closed
    )


    print(result)

    assert result["status"] == "WIN"
    assert memory.history["BTCUSDT"]["wins"] == 1


    print(
        "\nTRADE FEEDBACK BRIDGE PASSED ✅"
    )


if __name__ == "__main__":
    run_test()
