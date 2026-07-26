from brain.learning_memory_v10_64 import (
    LearningMemoryV10_64
)


print(
    "========== LEARNING MEMORY TEST V10.64 =========="
)


memory = LearningMemoryV10_64()


reward_record = {
    "position_id": 1,
    "symbol": "BTCUSDT",
    "reward": 1.0,
    "outcome": "WIN",
    "realized_pnl": 400.0
}


stored = memory.record(
    reward_record
)


print(
    "STORED EVENT:"
)

print(
    stored
)


summary = memory.summary()


print(
    "MEMORY SUMMARY:"
)

print(
    summary
)


assert stored["symbol"] == "BTCUSDT"

assert stored["reward"] == 1.0

assert summary["total_events"] == 1

assert summary["positive_events"] == 1

assert summary["negative_events"] == 0


print()

print(
    "✅ LEARNING MEMORY TEST V10.64 PASSED"
)
