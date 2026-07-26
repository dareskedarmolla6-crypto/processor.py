import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator
from brain.risk_engine import RiskEngine
from brain.risk_governor import RiskGovernor


def run_test():

    db = "risk_governor_brain.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== RISK GOVERNOR BRAIN ==========")


    # -------------------------
    # MEMORY + LEARNING
    # -------------------------

    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)


    trades = [

        {"symbol":"BTCUSDT","pnl":200},
        {"symbol":"BTCUSDT","pnl":150},

        {"symbol":"ETHUSDT","pnl":-100},
        {"symbol":"ETHUSDT","pnl":-50},

        {"symbol":"SOLUSDT","pnl":120},
        {"symbol":"SOLUSDT","pnl":100}

    ]


    for trade in trades:

        handler.process_closed_position({

            "symbol": trade["symbol"],
            "status": "CLOSED",
            "realized_pnl": trade["pnl"]

        })


    brain_state = optimizer.optimize()


    print("\nBRAIN STATE:")
    print(brain_state)



    # -------------------------
    # CAPITAL ALLOCATION
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


    print("\nALLOCATIONS:")
    print(allocations)



    # -------------------------
    # RISK GOVERNOR
    # -------------------------

    risk_engine = RiskEngine()

    governor = RiskGovernor(
        risk_engine
    )


    print("\nGOVERNOR DECISIONS:")


    for item in allocations:

        decision = governor.approve(

            symbol=item["symbol"],

            allocation=item["allocation"],

            status=item["status"],

            balance=1000,

            open_positions=[]

        )


        print(decision)



    print("\nFINAL MEMORY:")
    print(memory.history)


    print("\nRISK GOVERNOR BRAIN PASSED ✅")



if __name__ == "__main__":
    run_test()
