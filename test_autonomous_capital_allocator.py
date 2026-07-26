import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.capital_allocator import CapitalAllocator


def run_test():

    db = "autonomous_capital_allocator.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS CAPITAL ALLOCATOR ==========")

    # -------------------------
    # LEARNING MEMORY
    # -------------------------
    memory = MemoryManager(db)
    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)
    optimizer = SelfOptimizer(memory)

    # -------------------------
    # CREATE EXPERIENCE
    # -------------------------
    history = [
        {"symbol": "BTCUSDT", "pnl": 200},
        {"symbol": "BTCUSDT", "pnl": 100},
        {"symbol": "ETHUSDT", "pnl": -80},
        {"symbol": "ETHUSDT", "pnl": -50},
        {"symbol": "SOLUSDT", "pnl": 150},
        {"symbol": "SOLUSDT", "pnl": 100}
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
    # CAPITAL ALLOCATION
    # -------------------------
    allocator = CapitalAllocator()
    total_capital = 1000

    print("\nALLOCATIONS:")

    # የተስተካከለው ክፍል
    allocation_input = []
    for symbol, report in brain_state["report"].items():
        allocation_input.append({
            "symbol": symbol,
            "score": report["score"],
            "status": report["status"],
            "pnl": report["pnl"]
        })

    allocations = allocator.allocate(
        total_capital,
        allocation_input
    )

    print(allocations)

    print("\nMEMORY:")
    print(memory.history)

if __name__ == "__main__":
    run_test()
