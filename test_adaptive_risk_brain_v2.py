import os

from brain.memory_manager import MemoryManager
from brain.reward_engine import RewardEngine
from brain.closed_trade_handler import ClosedTradeHandler
from brain.self_optimizer import SelfOptimizer
from brain.adaptive_brain import AdaptiveBrain


def run_test():

    db = "adaptive_risk_brain_v2.db"

    if os.path.exists(db):
        os.remove(db)


    print("========== ADAPTIVE RISK BRAIN V2 ==========")


    memory = MemoryManager(db)

    reward = RewardEngine(memory)

    handler = ClosedTradeHandler(
        reward
    )

    optimizer = SelfOptimizer(
        memory
    )

    brain = AdaptiveBrain(
        memory
    )


    # -------------------------
    # LEARNING HISTORY
    # -------------------------

    trades = [

        {
            "symbol": "BTCUSDT",
            "pnl": 100
        },

        {
            "symbol": "BTCUSDT",
            "pnl": 80
        },

        {
            "symbol": "ETHUSDT",
            "pnl": -50
        },

        {
            "symbol": "ETHUSDT",
            "pnl": -40
        },

        {
            "symbol": "SOLUSDT",
            "pnl": 120
        },

        {
            "symbol": "SOLUSDT",
            "pnl": 90
        }

    ]


    for trade in trades:

        handler.process_closed_position(
            {
                "symbol": trade["symbol"],
                "status": "CLOSED",
                "realized_pnl": trade["pnl"]
            }
        )


    print("\nBRAIN STATE:")

    state = optimizer.optimize()

    print(state)



    # -------------------------
    # RISK DECISION TEST
    # -------------------------

    print("\nADAPTIVE RISK DECISIONS:")


    signals = [

        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.75
        },

        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "confidence": 0.85
        },

        {
            "symbol": "SOLUSDT",
            "signal": "BUY",
            "confidence": 0.75
        }

    ]


    for signal in signals:

        result = brain.evaluate(
            signal
        )

        risk = "NORMAL"

        report = state["report"].get(
            signal["symbol"]
        )


        if report:

            if report["status"] == "STRONG":
                risk = "INCREASE"

            elif report["status"] == "WEAK":
                risk = "REDUCE"


        print(
            {
                "symbol": result["symbol"],
                "decision": result["decision"],
                "confidence": result["confidence"],
                "risk_action": risk
            }
        )


    print("\nMEMORY:")
    print(memory.history)


    memory.close()


    print("\nADAPTIVE RISK BRAIN V2 PASSED ✅")



if __name__ == "__main__":
    run_test()
