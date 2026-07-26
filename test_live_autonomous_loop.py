import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.adaptive_brain import AdaptiveBrain

from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.price_monitor import PriceMonitor


def run_test():

    db = "live_autonomous_loop.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== LIVE AUTONOMOUS LOOP ==========")


    # -------------------------
    # MEMORY + LEARNING
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
    # EXECUTION SYSTEM
    # -------------------------
    execution = ExecutionEngine()


    manager = PositionManager(
        execution
    )


    monitor = PriceMonitor(
        manager
    )


    # -------------------------
    # PREVIOUS EXPERIENCE
    # -------------------------

    memory.record(
        "BTCUSDT",
        100
    )

    memory.record(
        "BTCUSDT",
        80
    )


    print("\nBRAIN BEFORE:")
    print(
        optimizer.optimize()
    )


    # -------------------------
    # NEW MARKET SIGNAL
    # -------------------------

    signal = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "confidence": 0.85
    }


    decision = brain.evaluate(
        signal
    )

    print("\nDECISION:")
    print(decision)


    # -------------------------
    # OPEN TRADE
    # -------------------------

    trade = manager.manage(
        "BTCUSDT",
        signal,
        price=50
    )

    print("\nOPEN:")
    print(trade)



    # -------------------------
    # PRICE MOVEMENT
    # -------------------------

    lock = monitor.update(
        "BTCUSDT",
        55
    )

    print("\nLOCK:")
    print(lock)


    exit_result = monitor.update(
        "BTCUSDT",
        53
    )

    print("\nEXIT:")
    print(exit_result)



    # -------------------------
    # CLOSED POSITION
    # -------------------------

    position = execution.positions["BTCUSDT"][0]

    print("\nCLOSED:")
    print(position)



    # -------------------------
    # LEARNING
    # -------------------------

    learning = handler.process_closed_position(
        position
    )


    print("\nLEARNING:")
    print(learning)


    print("\nMEMORY:")
    print(memory.history)


    print("\nOPTIMIZER AFTER:")
    print(
        optimizer.optimize()
    )


    memory.close()

    print("\nLIVE AUTONOMOUS LOOP PASSED ✅")



if __name__ == "__main__":
    run_test()
