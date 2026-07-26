from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator
from brain.risk_engine import RiskEngine


def run_test():

    print("========== CAPITAL RISK BRAIN ==========")

    memory = MemoryManager("capital_risk_brain.db")

    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)

    optimizer = SelfOptimizer(memory)


    # -------------------------
    # EXPERIENCE
    # -------------------------

    trades = [

        {"symbol":"BTCUSDT","pnl":200},
        {"symbol":"BTCUSDT","pnl":150},

        {"symbol":"ETHUSDT","pnl":-100},
        {"symbol":"ETHUSDT","pnl":-50},

        {"symbol":"SOLUSDT","pnl":120},
        {"symbol":"SOLUSDT","pnl":100}

    ]


    for t in trades:

        handler.process_closed_position({
            "symbol":t["symbol"],
            "status":"CLOSED",
            "realized_pnl":t["pnl"]
        })


    brain = optimizer.optimize()


    print("\nBRAIN:")
    print(brain)



    # -------------------------
    # CAPITAL
    # -------------------------

    allocator = CapitalAllocator()

    assets=[]

    for symbol,data in brain["report"].items():

        assets.append({

            "symbol":symbol,
            "score":data["score"],
            "status":data["status"],
            "pnl":data["pnl"]

        })


    allocation = allocator.allocate(
        1000,
        assets
    )


    print("\nCAPITAL:")
    print(allocation)



    # -------------------------
    # RISK CHECK
    # -------------------------

    risk = RiskEngine()


    print("\nRISK CHECK:")

    for item in allocation:

        result = risk.check_trade(
            balance=1000,
            position_size=item["allocation"],
            open_positions=[]
        )

        print(
            item["symbol"],
            "=>",
            result
        )


    print("\nCAPITAL RISK BRAIN PASSED ✅")


if __name__=="__main__":
    run_test()
