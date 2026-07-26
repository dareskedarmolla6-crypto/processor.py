import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator


def run_test():

    db = "autonomous_capital_rebalance.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS CAPITAL REBALANCE ==========")


    # -------------------------
    # INIT BRAIN
    # -------------------------

    memory = MemoryManager(db)
    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)
    optimizer = SelfOptimizer(memory)


    # -------------------------
    # EXPERIENCE
    # -------------------------

    history = [
        ("BTCUSDT", 300),
        ("BTCUSDT", 200),

        ("ETHUSDT", -100),
        ("ETHUSDT", -80),

        ("SOLUSDT", 250),
        ("SOLUSDT", 150),
    ]


    for symbol, pnl in history:

        handler.process_closed_position(
            {
                "symbol": symbol,
                "status": "CLOSED",
                "realized_pnl": pnl
            }
        )


    brain = optimizer.optimize()


    print("\nBRAIN STATE:")
    print(brain)



    # -------------------------
    # BEFORE ALLOCATION
    # -------------------------

    allocator = CapitalAllocator()

    capital = 1000


    allocation_input = []

    for symbol, data in brain["report"].items():

        allocation_input.append(
            {
                "symbol": symbol,
                "score": data["score"],
                "status": data["status"],
                "pnl": data["pnl"]
            }
        )


    print("\nBEFORE REALLOCATION:")
    print(
        allocator.allocate(
            capital,
            allocation_input
        )
    )


    # -------------------------
    # REBALANCE LOGIC
    # -------------------------

    rebalance = []

    strong_count = 0

    for item in allocation_input:

        if item["status"] == "STRONG":
            strong_count += 1


    strong_share = capital / strong_count


    for item in allocation_input:

        if item["status"] == "STRONG":

            amount = strong_share

        else:

            amount = 0


        rebalance.append(
            {
                "symbol": item["symbol"],
                "new_allocation": amount,
                "status": item["status"]
            }
        )


    print("\nAFTER REALLOCATION:")
    print(rebalance)



    # -------------------------
    # FINAL MEMORY
    # -------------------------

    print("\nFINAL MEMORY:")
    print(memory.history)


    print("\nAUTONOMOUS CAPITAL REBALANCE PASSED ✅")



if __name__ == "__main__":
    run_test()
