from brain.execution_engine import ExecutionEngine
from brain.trade_feedback_engine_v10_61 import (
    TradeFeedbackEngineV10_61
)

from brain.performance_memory_v10_62 import (
    PerformanceMemoryV10_62
)


print(
    "========== PERFORMANCE MEMORY TEST V10.62 =========="
)


feedback_engine = TradeFeedbackEngineV10_61()


memory = PerformanceMemoryV10_62()


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


feedback = result["feedback"]


stored = memory.store(
    feedback
)


print("STORED FEEDBACK:")
print(stored)


stats = memory.statistics()


print("STATISTICS:")
print(stats)


assert stats["total_trades"] == 1

assert stats["wins"] == 1

assert stats["losses"] == 0

assert stats["total_pnl"] == 400.0


print()

print(
    "✅ PERFORMANCE MEMORY TEST V10.62 PASSED"
)
