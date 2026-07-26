import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator
from brain.risk_governor import RiskGovernor
from brain.execution_engine import ExecutionEngine
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    db = "full_autonomous_brain_controller_v4.db"

    if os.path.exists(db):
        os.remove(db)


    print("========== FULL AUTONOMOUS BRAIN CONTROLLER V4 ==========")


    # -------------------------
    # CORE
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)

    adaptive_brain = AdaptiveBrain(memory)

    allocator = CapitalAllocator()

    governor = RiskGovernor()

    execution = ExecutionEngine()



    # -------------------------
    # OLD EXPERIENCE
    # -------------------------

    history = [

        ("BTCUSDT", 300),
        ("BTCUSDT", 200),

        ("ETHUSDT", -120),

        ("SOLUSDT", 250)

    ]


    for symbol, pnl in history:

        handler.process_closed_position(
            {
                "symbol": symbol,
                "status": "CLOSED",
                "realized_pnl": pnl
            }
        )


    brain_state = optimizer.optimize()


    print("\nINITIAL BRAIN:")
    print(brain_state)



    # -------------------------
    # MULTI SIGNALS
    # -------------------------

    signals = [

        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.95
        },

        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "confidence": 0.75
        },

        {
            "symbol": "SOLUSDT",
            "signal": "BUY",
            "confidence": 0.90
        }

    ]



    # -------------------------
    # ALLOCATE CAPITAL
    # -------------------------

    allocation_input = []


    for symbol, data in brain_state["report"].items():

        allocation_input.append(
            {
                "symbol": symbol,
                "score": data["score"],
                "status": data["status"],
                "pnl": data["pnl"]
            }
        )


    capital = allocator.allocate(
        1000,
        allocation_input
    )


    print("\nCAPITAL:")
    print(capital)



    # -------------------------
    # AUTONOMOUS LOOP
    # -------------------------

    positions = []


    print("\nDECISIONS:")


    for signal in signals:


        decision = adaptive_brain.evaluate(signal)


        print(decision)


        if decision["decision"] != "TRADE":
            continue



        allocation = next(
            (
                x for x in capital
                if x["symbol"] == signal["symbol"]
            ),
            None
        )


        if allocation is None:
            continue



        risk = governor.approve(

            signal["symbol"],

            allocation["allocation"],

            allocation["status"],

            1000,

            positions

        )


        print("RISK:")
        print(risk)



        if risk["decision"] != "APPROVED":
            continue



        position = execution.open(

            signal["symbol"],

            "LONG",

            1,

            50

        )


        positions.append(position)


        print("OPEN:")
        print(position)



    # -------------------------
    # CLOSE ALL POSITIONS
    # -------------------------

    print("\nLEARNING:")


    for position in positions:


        position["status"] = "CLOSED"

        if position["symbol"] == "ETHUSDT":

            position["realized_pnl"] = -30

        else:

            position["realized_pnl"] = 60


        position["exit"] = 55



        result = handler.process_closed_position(
            position
        )


        print(result)



    # -------------------------
    # FINAL STATE
    # -------------------------

    final = optimizer.optimize()


    print("\nFINAL BRAIN:")
    print(final)


    print("\nFINAL MEMORY:")
    print(memory.history)


    print("\nFULL AUTONOMOUS BRAIN CONTROLLER V4 PASSED ✅")



if __name__ == "__main__":
    run_test()
