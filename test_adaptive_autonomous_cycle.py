import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.smart_exit import SmartExit
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    db = "adaptive_cycle.db"

    if os.path.exists(db):
        os.remove(db)


    print("========== ADAPTIVE AUTONOMOUS CYCLE ==========")


    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)


    brain = AdaptiveBrain(memory)


    execution = ExecutionEngine()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )

    smart = SmartExit()


    manager = PositionManager(
        execution,
        smart,
        risk
    )


    # -----------------------
    # LEARN HISTORY
    # -----------------------

    history = [
        ("BTCUSDT",100),
        ("BTCUSDT",80),
        ("ETHUSDT",-50),
        ("ETHUSDT",-30),
        ("SOLUSDT",120),
    ]


    for symbol,pnl in history:

        reward.evaluate(
            symbol,
            pnl
        )


    print("\nBRAIN STATE:")
    print(
        brain.optimize()
    )


    # -----------------------
    # NEW MARKET DECISION
    # -----------------------

    signal = {
        "signal":"BUY",
        "confidence":0.85
    }


    trade = manager.manage(
        "BTCUSDT",
        signal,
        price=50,
        balance=1000,
        stop_loss_price=49
    )


    print("\nOPEN:")
    print(trade)



    # -----------------------
    # PRICE MOVEMENT
    # -----------------------

    lock = manager.manage(
        "BTCUSDT",
        {"signal":"BUY"},
        price=55
    )

    print("\nLOCK:")
    print(lock)


    exit_result = manager.manage(
        "BTCUSDT",
        {"signal":"BUY"},
        price=53
    )


    print("\nEXIT:")
    print(exit_result)



    closed = execution.positions["BTCUSDT"][0]


    print("\nCLOSED:")
    print(closed)


    learn = handler.process_closed_position(
        closed
    )


    print("\nLEARNING:")
    print(learn)


    print("\nFINAL MEMORY:")
    print(memory.history)


    memory.close()


    print("\nADAPTIVE AUTONOMOUS CYCLE PASSED ✅")



if __name__ == "__main__":
    run_test()
