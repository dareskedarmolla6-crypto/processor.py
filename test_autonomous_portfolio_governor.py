import os
from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator
from brain.risk_governor import RiskGovernor

def run_test():
    db = "autonomous_portfolio_governor.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS PORTFOLIO GOVERNOR ==========")

    # -------------------------
    # INIT
    # -------------------------
    memory = MemoryManager(db)
    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)
    optimizer = SelfOptimizer(memory)
    governor = RiskGovernor()

    # -------------------------
    # LEARNING HISTORY
    # -------------------------
    history = [
        ("BTCUSDT", 300),
        ("BTCUSDT", 200),
        ("ETHUSDT", -120),
        ("ETHUSDT", -80),
        ("SOLUSDT", 250),
        ("SOLUSDT", 150)
    ]

    for symbol, pnl in history:
        handler.process_closed_position({
            "symbol": symbol,
            "status": "CLOSED",
            "realized_pnl": pnl
        })

    brain = optimizer.optimize()

    print("\nBRAIN STATE:")
    print(brain)

    # -------------------------
    # CAPITAL
    # -------------------------
    allocator = CapitalAllocator()
    allocation_input = []

    for symbol, data in brain["report"].items():
        allocation_input.append({
            "symbol": symbol,
            "score": data["score"],
            "status": data["status"],
            "pnl": data["pnl"]
        })

    capital = allocator.allocate(1000, allocation_input)

    print("\nCAPITAL:")
    print(capital)

    # -------------------------
    # GOVERNOR CHECK
    # -------------------------
    print("\nGOVERNOR DECISIONS:")

    for item in capital:
        # አሁን በ approve() ሜተድ በኩል ውሳኔዎችን እንጠይቃለን
        decision = governor.approve(
            item["symbol"],
            item["allocation"],
            item["status"],
            1000,  # Total Capital
            []     # Open Positions
        )

        print({
            "symbol": item["symbol"],
            "decision": decision
        })

    # -------------------------
    # FINAL
    # -------------------------
    print("\nFINAL MEMORY:")
    print(memory.history)

    print("\nAUTONOMOUS PORTFOLIO GOVERNOR PASSED ✅")

if __name__ == "__main__":
    run_test()
