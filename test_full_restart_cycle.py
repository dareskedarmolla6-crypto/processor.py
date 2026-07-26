import os
from brain.memory_manager import MemoryManager
from brain.autonomous_brain import AutonomousBrain
from brain.reward_engine import RewardEngine
from brain.feedback_loop import FeedbackLoop
from brain.self_optimizer import SelfOptimizer

def run_test():
    db = "full_cycle_test.db"

    # አዲስ ሙከራ ከመጀመሩ በፊት የድሮውን ዳታቤዝ በራስ-ሰር ይሰርዛል
    if os.path.exists(db):
        os.remove(db)

    print("========== FULL RESTART CYCLE TEST ==========")

    # =====================
    # START SYSTEM
    # =====================
    memory = MemoryManager(db)
    
    optimizer = SelfOptimizer(memory.live_memory)
    brain = AutonomousBrain(memory.live_memory)
    reward = RewardEngine(memory.live_memory)
    
    # እዚህ ጋር memory ብቻ ተቀይሯል
    feedback = FeedbackLoop(
        reward,
        memory,
        optimizer
    )

    # =====================
    # MARKET INPUT
    # =====================
    signals = [
        {"symbol": "BTCUSDT", "signal": "BUY", "price": 60000, "confidence": 0.75},
        {"symbol": "ETHUSDT", "signal": "BUY", "price": 3000, "confidence": 0.75}
    ]

    result = brain.run_cycle(signals)
    print("\nBRAIN:")
    print(result)

    # =====================
    # FEEDBACK
    # =====================
    feedback_result = feedback.process_batch([
        {"symbol": "BTCUSDT", "pnl": 100},
        {"symbol": "ETHUSDT", "pnl": -50}
    ])
    print("\nFEEDBACK:")
    print(feedback_result)

    # Save to SQLite
    memory.close()

    # =====================
    # RESTART
    # =====================
    memory2 = MemoryManager(db)
    print("\nAFTER RESTART:")
    print(memory2.history)

    # አሁን ዳታቤዙ በየጊዜው ስለሚጸዳ እነዚህ ሁልጊዜ 1 መሆናቸውን ያረጋግጣሉ
    assert memory2.history["BTCUSDT"]["wins"] == 1
    assert memory2.history["ETHUSDT"]["losses"] == 1

    memory2.close()
    
    # ሙከራው ካለቀ በኋላ ማጽዳት (አማራጭ ነው)
    if os.path.exists(db):
        os.remove(db)
                                                                                                                                                
    print("\nFULL RESTART CYCLE TEST PASSED ✅")

if __name__ == "__main__":
    run_test()
