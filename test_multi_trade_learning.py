import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.self_optimizer import SelfOptimizer  # የተስተካከለ import


def run_test():

    db = "multi_trade_learning.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== MULTI TRADE LEARNING TEST ==========")

    # Memory
    memory = MemoryManager(db)

    # Reward System
    reward = RewardEngine(memory)

    trades = [
        {"symbol": "BTCUSDT", "pnl": 100},
        {"symbol": "ETHUSDT", "pnl": -50},
        {"symbol": "SOLUSDT", "pnl": 80},
        {"symbol": "BTCUSDT", "pnl": -20}
    ]

    print("\nFEEDBACK:")

    results = []

    for trade in trades:
        # reward.evaluate የሚለው ከሪዋርድ ሞጁልህ ጋር የሚሄድ መሆኑን አረጋግጥ
        result = reward.evaluate(
            trade["symbol"],
            trade["pnl"]
        )

        results.append(result)
        print(result)

    print("\nMEMORY:")
    print(memory.history)

    # SelfOptimizer አጠቃቀም
    optimizer = SelfOptimizer(memory)

    print("\nOPTIMIZER:")
    print(
        optimizer.optimize()
    )

    memory.close()

    print("\nMULTI TRADE LEARNING PASSED ✅")


if __name__ == "__main__":
    run_test()
