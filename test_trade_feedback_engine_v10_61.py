from brain.trade_feedback_engine_v10_61 import (
    TradeFeedbackEngineV10_61
)

from brain.execution_engine import ExecutionEngine


print(
    "========== TRADE FEEDBACK INTEGRATION TEST V10.61 =========="
)


feedback_engine = TradeFeedbackEngineV10_61()


execution = ExecutionEngine(
    feedback_engine=feedback_engine
)


position = execution.open(
    "BTCUSDT",
    "LONG",
    0.2,
    50000
)


result = execution.close_by_id(
    "BTCUSDT",
    position["id"],
    52000,
    "TAKE_PROFIT"
)


print("CLOSE RESULT:")
print(result)


assert result["position"]["status"] == "CLOSED"

assert (
    result["feedback"]["outcome"]
    == "WIN"
)

assert (
    result["feedback"]["realized_pnl"]
    > 0
)


print()

print(
    "✅ TRADE FEEDBACK INTEGRATION TEST V10.61 PASSED"
)
