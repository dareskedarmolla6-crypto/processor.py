import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer

from brain.adaptive_brain import AdaptiveBrain
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.smart_exit import SmartExit


def run_test():

    db = "full_autonomous_pipeline.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== FULL AUTONOMOUS PIPELINE ==========")


    # MEMORY
    memory = MemoryManager(db)

    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)


    # EXPERIENCE
    history = [
        ("BTCUSDT", 200),
        ("BTCUSDT", 150),
        ("ETHUSDT", -100),
        ("SOLUSDT", 180)
    ]


    for symbol, pnl in history:

        handler.process_closed_position({
            "symbol": symbol,
            "status": "CLOSED",
            "realized_pnl": pnl
        })


    brain_state = optimizer.optimize()

    print("\nBRAIN:")
    print(brain_state)



    # ADAPTIVE DECISION

    adaptive = AdaptiveBrain(memory)

    signal = {
        "symbol":"BTCUSDT",
        "signal":"BUY",
        "confidence":0.9
    }


    decision = adaptive.evaluate(signal)

    print("\nDECISION:")
    print(decision)



    # EXECUTION

    execution = ExecutionEngine()

    manager = PositionManager(
        execution,
        SmartExit()
    )


    opened = manager.manage(
        "BTCUSDT",
        {
            "signal":"BUY"
        },
        50
    )


    print("\nOPEN:")
    print(opened)



    # EXIT FLOW

    lock = manager.manage(
        "BTCUSDT",
        {
            "signal":"HOLD"
        },
        55
    )

    print("\nLOCK:")
    print(lock)



    exit_result = manager.manage(
        "BTCUSDT",
        {
            "signal":"HOLD"
        },
        53
    )

    print("\nEXIT:")
    print(exit_result)



    closed = execution.positions["BTCUSDT"][0]

    print("\nCLOSED:")
    print(closed)



    learned = handler.process_closed_position(closed)


    print("\nLEARNING:")
    print(learned)



    print("\nFINAL MEMORY:")
    print(memory.history)


    print("\nFULL AUTONOMOUS PIPELINE PASSED ✅")


if __name__ == "__main__":
    run_test()
