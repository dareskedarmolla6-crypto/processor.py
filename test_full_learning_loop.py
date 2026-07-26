import os

from brain.memory_manager import MemoryManager
from brain.autonomous_brain import AutonomousBrain
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer


def run_test():

    print("========== FULL AUTONOMOUS LEARNING LOOP ==========")


    db = "full_learning_loop.db"

    if os.path.exists(db):
        os.remove(db)


    # =========================
    # MEMORY + LEARNING
    # =========================

    memory = MemoryManager(db)

    reward = RewardEngine(
        memory
    )

    handler = ClosedTradeHandler(
        reward
    )

    optimizer = SelfOptimizer(
        memory.live_memory
    )


    # =========================
    # BRAIN
    # =========================

    brain = AutonomousBrain(
        memory.live_memory
    )


    signals = [
        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "price": 50,
            "confidence": 0.85
        }
    ]


    brain_result = brain.run_cycle(
        signals
    )

    print("\nBRAIN:")
    print(brain_result)



    # =========================
    # EXECUTION PIPELINE
    # =========================

    execution = ExecutionEngine()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )

    smart_exit = SmartExit()


    manager = PositionManager(
        execution,
        smart_exit,
        risk
    )


    # OPEN TRADE

    trade = manager.manage(
        "BTCUSDT",
        {
            "signal": "BUY"
        },
        price=50,
        balance=1000,
        stop_loss_price=49
    )


    print("\nOPEN:")
    print(trade)



    position = trade["position"]



    # =========================
    # PROFIT LOCK
    # =========================

    lock = manager.manage(
        "BTCUSDT",
        {
            "signal": "HOLD"
        },
        price=55
    )

    print("\nLOCK:")
    print(lock)



    # =========================
    # TRAILING EXIT
    # =========================

    exit_result = manager.manage(
        "BTCUSDT",
        {
            "signal": "HOLD"
        },
        price=53
    )

    print("\nEXIT:")
    print(exit_result)



    closed_position = execution.positions["BTCUSDT"][0]


    print("\nCLOSED POSITION:")
    print(closed_position)



    # =========================
    # LEARNING
    # =========================

    learning = handler.process_closed_position(
        {
            "symbol": "BTCUSDT",
            "status": "CLOSED",
            "realized_pnl": closed_position["realized_pnl"]
        }
    )


    print("\nLEARNING:")
    print(learning)



    print("\nMEMORY:")
    print(memory.history)



    print("\nOPTIMIZER:")
    print(
        optimizer.optimize()
    )


    memory.close()


    print(
        "\nFULL AUTONOMOUS LEARNING LOOP PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
