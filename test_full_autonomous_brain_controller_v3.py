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

    db = "full_autonomous_brain_controller_v3.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== FULL AUTONOMOUS BRAIN CONTROLLER V3 ==========")


    # -------------------------
    # CORE SYSTEMS
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)

    brain_optimizer = optimizer

    capital_allocator = CapitalAllocator()

    governor = RiskGovernor()

    execution = ExecutionEngine()

    adaptive_brain = AdaptiveBrain(memory)



    # -------------------------
    # PREVIOUS EXPERIENCE
    # -------------------------

    history = [

        ("BTCUSDT", 300),
        ("BTCUSDT", 200),

        ("ETHUSDT", -100),

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


    brain_state = brain_optimizer.optimize()


    print("\nBRAIN STATE:")
    print(brain_state)



    # -------------------------
    # NEW SIGNAL
    # -------------------------

    signal = {

        "symbol": "BTCUSDT",

        "signal": "BUY",

        "confidence": 0.95

    }


    decision = adaptive_brain.evaluate(signal)


    print("\nBRAIN DECISION:")
    print(decision)



    if decision["decision"] != "TRADE":

        print("TRADE BLOCKED")

        return



    # -------------------------
    # CAPITAL
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


    capital = capital_allocator.allocate(
        1000,
        allocation_input
    )


    print("\nCAPITAL:")
    print(capital)



    btc = next(
        x for x in capital
        if x["symbol"] == "BTCUSDT"
    )



    risk = governor.approve(

        btc["symbol"],

        btc["allocation"],

        btc["status"],

        1000,

        []

    )


    print("\nRISK:")
    print(risk)



    if risk["decision"] != "APPROVED":

        print("RISK BLOCKED")

        return



    # -------------------------
    # EXECUTION
    # -------------------------

    opened = execution.open(

        "BTCUSDT",

        "LONG",

        1,

        50

    )


    print("\nOPEN:")
    print(opened)



    position = opened



    # simulate close

    position["status"] = "CLOSED"

    position["realized_pnl"] = 80

    position["exit"] = 55



    learned = handler.process_closed_position(
        position
    )


    print("\nLEARNING:")
    print(learned)



    # -------------------------
    # FINAL
    # -------------------------

    final_brain = optimizer.optimize()


    print("\nFINAL BRAIN:")
    print(final_brain)


    print("\nFINAL MEMORY:")
    print(memory.history)


    print("\nFULL AUTONOMOUS BRAIN CONTROLLER V3 PASSED ✅")



if __name__ == "__main__":
    run_test()
