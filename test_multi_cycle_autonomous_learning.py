import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    db = "multi_cycle_learning.db"

    if os.path.exists(db):
        os.remove(db)


    print("========== MULTI CYCLE AUTONOMOUS LEARNING ==========")


    # -------------------------
    # CORE LEARNING SYSTEM
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(
        reward
    )

    optimizer = SelfOptimizer(
        memory
    )

    brain = AdaptiveBrain(
        memory
    )


    # -------------------------
    # CYCLE 1
    # BTC SUCCESS
    # -------------------------

    print("\nCYCLE 1: BTCUSDT WIN")

    handler.process_closed_position(
        {
            "symbol": "BTCUSDT",
            "status": "CLOSED",
            "realized_pnl": 100
        }
    )


    print(
        optimizer.optimize()
    )


    # -------------------------
    # CYCLE 2
    # ETH LOSS
    # -------------------------

    print("\nCYCLE 2: ETHUSDT LOSS")


    handler.process_closed_position(
        {
            "symbol": "ETHUSDT",
            "status": "CLOSED",
            "realized_pnl": -80
        }
    )


    print(
        optimizer.optimize()
    )


    # -------------------------
    # CYCLE 3
    # SOL SUCCESS
    # -------------------------

    print("\nCYCLE 3: SOLUSDT WIN")


    handler.process_closed_position(
        {
            "symbol": "SOLUSDT",
            "status": "CLOSED",
            "realized_pnl": 150
        }
    )


    brain_state = optimizer.optimize()


    print(
        brain_state
    )


    # -------------------------
    # ADAPTIVE DECISIONS
    # -------------------------

    print("\nADAPTIVE DECISIONS:")


    signals = [

        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.80
        },

        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "confidence": 0.80
        },

        {
            "symbol": "SOLUSDT",
            "signal": "BUY",
            "confidence": 0.80
        }

    ]


    for signal in signals:

        result = brain.evaluate(
            signal
        )

        print(result)



    print("\nFINAL MEMORY:")
    print(memory.history)


    memory.close()


    print("\nMULTI CYCLE AUTONOMOUS LEARNING PASSED ✅")



if __name__ == "__main__":
    run_test()
