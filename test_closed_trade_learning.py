import os
from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler

def run_test():
    db = "closed_learning.db"
    
    # የድሮውን ዳታቤዝ አጽዳ
    if os.path.exists(db):
        os.remove(db)

    print("========== CLOSED TRADE LEARNING TEST ==========")

    # PersistentMemory ፈንታ MemoryManager እንጠቀማለን
    memory = MemoryManager(db)

    # RewardEngine እና Handler ወደ MemoryManager ይጠቁማሉ
    reward = RewardEngine(memory)
    handler = ClosedTradeHandler(reward)

    closed_trade = {
        "symbol": "BTCUSDT",
        "status": "CLOSED",
        "realized_pnl": 90
    }

    result = handler.process_closed_position(closed_trade)
    print(result)

    print("\nMEMORY:")
    print(memory.history)

    memory.close()

    print("\nCLOSED TRADE LEARNING PASSED ✅")

if __name__ == "__main__":
    run_test()
