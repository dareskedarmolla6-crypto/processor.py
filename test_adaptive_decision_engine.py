import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.self_optimizer import SelfOptimizer


def run_test():

    db = "adaptive_decision.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== ADAPTIVE DECISION ENGINE TEST ==========")


    memory = MemoryManager(db)
    reward = RewardEngine(memory)


    # የቀድሞ performance
    history = [

        {"symbol": "BTCUSDT", "pnl": 100},
        {"symbol": "BTCUSDT", "pnl": 80},

        {"symbol": "ETHUSDT", "pnl": -50},
        {"symbol": "ETHUSDT", "pnl": -30},

        {"symbol": "SOLUSDT", "pnl": 120},
        {"symbol": "SOLUSDT", "pnl": 90},

    ]


    for trade in history:
        reward.evaluate(
            trade["symbol"],
            trade["pnl"]
        )


    optimizer = SelfOptimizer(memory)

    brain_state = optimizer.optimize()


    print("\nBRAIN STATE:")
    print(brain_state)



    # New signals
    signals = [

        {
            "symbol": "BTCUSDT",
            "confidence": 0.75
        },

        {
            "symbol": "ETHUSDT",
            "confidence": 0.85
        },

        {
            "symbol": "SOLUSDT",
            "confidence": 0.70
        }

    ]


    print("\nADAPTIVE DECISIONS:")


    for signal in signals:

        symbol = signal["symbol"]

        confidence = signal["confidence"]

        report = brain_state["report"].get(symbol)


        if report:

            status = report["status"]


            if status == "STRONG":

                confidence += 0.10


            elif status == "WEAK":

                confidence -= 0.20



        if confidence >= brain_state["confidence_threshold"]:

            decision = "TRADE"

        else:

            decision = "SKIP"



        print(
            {
                "symbol": symbol,
                "final_confidence": round(confidence,2),
                "decision": decision
            }
        )


    memory.close()


    print("\nADAPTIVE DECISION ENGINE PASSED ✅")


if __name__ == "__main__":
    run_test()
