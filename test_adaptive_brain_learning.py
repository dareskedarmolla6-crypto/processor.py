import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.self_optimizer import SelfOptimizer


def run_test():

    db = "adaptive_brain_learning.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== ADAPTIVE BRAIN LEARNING TEST ==========")


    memory = MemoryManager(db)
    reward = RewardEngine(memory)


    # Historical performance
    trades = [

        {"symbol": "BTCUSDT", "pnl": 100},
        {"symbol": "BTCUSDT", "pnl": 80},

        {"symbol": "ETHUSDT", "pnl": -50},
        {"symbol": "ETHUSDT", "pnl": -30},

        {"symbol": "SOLUSDT", "pnl": 120},
        {"symbol": "SOLUSDT", "pnl": 90},

    ]


    print("\nLEARNING FEEDBACK:")

    for trade in trades:

        result = reward.evaluate(
            trade["symbol"],
            trade["pnl"]
        )

        print(result)



    print("\nMEMORY:")
    print(memory.history)



    optimizer = SelfOptimizer(memory)


    optimized = optimizer.optimize()


    print("\nADAPTIVE RESULT:")
    print(optimized)


    print("\nDECISION TEST:")

    report = optimized["report"]


    for symbol, data in report.items():

        if data["status"] == "STRONG":
            decision = "INCREASE_CONFIDENCE"

        elif data["status"] == "WEAK":
            decision = "REDUCE_EXPOSURE"

        else:
            decision = "NORMAL_MODE"


        print(
            symbol,
            "=>",
            decision
        )


    memory.close()


    print("\nADAPTIVE BRAIN LEARNING PASSED ✅")


if __name__ == "__main__":
    run_test()
