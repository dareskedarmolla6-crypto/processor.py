from brain.reward_engine_v10_63 import (
    RewardEngineV10_63
)


print(
    "========== REWARD ENGINE TEST V10.63 =========="
)


feedback = {
    "position_id": 1,
    "symbol": "BTCUSDT",
    "side": "LONG",
    "entry_price": 50000,
    "exit_price": 52000,
    "realized_pnl": 400.0,
    "outcome": "WIN",
    "closed_at": "2026-07-14T05:00:00+00:00"
}


engine = RewardEngineV10_63()


reward = engine.calculate(
    feedback
)


print(
    "REWARD RESULT:"
)

print(
    reward
)


assert reward["position_id"] == 1

assert reward["symbol"] == "BTCUSDT"

assert reward["reward"] == 1.0

assert reward["outcome"] == "WIN"


print()

print(
    "✅ REWARD ENGINE TEST V10.63 PASSED"
)
