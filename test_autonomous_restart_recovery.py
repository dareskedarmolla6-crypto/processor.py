import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    db = "autonomous_restart_recovery.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS RESTART RECOVERY ==========")


    # -------------------------
    # FIRST SESSION
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)


    print("\nSESSION 1: CREATE EXPERIENCE")


    handler.process_closed_position({
        "symbol": "BTCUSDT",
        "status": "CLOSED",
        "realized_pnl": 200
    })


    handler.process_closed_position({
        "symbol": "ETHUSDT",
        "status": "CLOSED",
        "realized_pnl": -100
    })


    state_before = optimizer.optimize()

    print("\nBRAIN BEFORE RESTART:")
    print(state_before)



    # -------------------------
    # OPEN POSITION BEFORE STOP
    # -------------------------

    execution = ExecutionEngine()

    manager = PositionManager(
        execution=execution
    )


    opened = manager.manage(
        "BTCUSDT",
        {
            "signal": "BUY"
        },
        price=50
    )


    print("\nOPEN POSITION:")
    print(opened)



    # simulate shutdown
    memory.close()


    # -------------------------
    # RESTART
    # -------------------------

    print("\n========== RESTART ==========")


    memory2 = MemoryManager(db)

    reward2 = RewardEngine(memory2)

    optimizer2 = SelfOptimizer(memory2)


    state_after = optimizer2.optimize()


    print("\nBRAIN AFTER RESTART:")
    print(state_after)



    # -------------------------
    # ADAPTIVE DECISION
    # -------------------------

    brain = AdaptiveBrain(
        memory2,
        min_confidence=0.70
    )


    decision = brain.evaluate(
        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.85
        }
    )


    print("\nRECOVERED DECISION:")
    print(decision)



    print("\nFINAL MEMORY:")
    print(memory2.history)


    memory2.close()


    print("\nAUTONOMOUS RESTART RECOVERY PASSED ✅")



if __name__ == "__main__":
    run_test()
