import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator
from brain.risk_engine import RiskEngine
from brain.risk_governor import RiskGovernor
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.smart_exit import SmartExit


def run_test():

    db = "autonomous_brain_controller.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS BRAIN CONTROLLER ==========")


    # -------------------------
    # LEARNING SYSTEM
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)


    # Experience

    history = [

        {"symbol":"BTCUSDT","pnl":200},
        {"symbol":"BTCUSDT","pnl":150},

        {"symbol":"ETHUSDT","pnl":-100},
        {"symbol":"ETHUSDT","pnl":-50},

        {"symbol":"SOLUSDT","pnl":120},
        {"symbol":"SOLUSDT","pnl":100}

    ]


    for item in history:

        handler.process_closed_position({

            "symbol": item["symbol"],
            "status": "CLOSED",
            "realized_pnl": item["pnl"]

        })


    brain_state = optimizer.optimize()


    print("\nBRAIN STATE:")
    print(brain_state)



    # -------------------------
    # CAPITAL
    # -------------------------

    allocator = CapitalAllocator()


    assets = []

    for symbol,data in brain_state["report"].items():

        assets.append({

            "symbol": symbol,
            "score": data["score"],
            "status": data["status"],
            "pnl": data["pnl"]

        })


    allocations = allocator.allocate(
        1000,
        assets
    )


    print("\nCAPITAL:")
    print(allocations)



    # -------------------------
    # EXECUTION SYSTEM
    # -------------------------

    execution = ExecutionEngine()

    smart_exit = SmartExit()

    position_manager = PositionManager(
        execution,
        smart_exit
    )


    # -------------------------
    # RISK GOVERNOR
    # -------------------------

    risk = RiskEngine()

    governor = RiskGovernor(risk)


    print("\nTRADING DECISION:")


    for item in allocations:


        permission = governor.approve(

            item["symbol"],
            item["allocation"],
            item["status"],
            1000,
            []

        )


        print(permission)



        if permission["decision"] == "APPROVED":


            signal = {

                "signal":"BUY"

            }


            result = position_manager.manage(

                item["symbol"],
                signal,
                50

            )


            print("EXECUTION:")
            print(result)



    print("\nMEMORY:")
    print(memory.history)


    print("\nAUTONOMOUS BRAIN CONTROLLER PASSED ✅")



if __name__ == "__main__":
    run_test()
