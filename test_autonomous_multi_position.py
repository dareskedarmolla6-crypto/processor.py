import os

from brain.autonomous_controller_v2 import AutonomousControllerV2


def run_test():

    db = "autonomous_multi_position.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== AUTONOMOUS MULTI POSITION ==========")


    controller = AutonomousControllerV2(db)


    # -----------------------------
    # CREATE EXPERIENCE
    # -----------------------------

    history = [
        ("BTCUSDT", 200),
        ("ETHUSDT", -100),
        ("SOLUSDT", 150),
    ]


    for symbol, pnl in history:

        controller.learn({
            "symbol": symbol,
            "status": "CLOSED",
            "realized_pnl": pnl
        })


    print("\nBRAIN STATE:")
    print(controller.optimize())


    # -----------------------------
    # OPEN MULTIPLE POSITIONS
    # -----------------------------

    signals = [
        {
            "symbol": "BTCUSDT",
            "signal": "BUY",
            "confidence": 0.95
        },
        {
            "symbol": "ETHUSDT",
            "signal": "BUY",
            "confidence": 0.80
        },
        {
            "symbol": "SOLUSDT",
            "signal": "BUY",
            "confidence": 0.90
        }
    ]


    print("\nDECISIONS:")

    for signal in signals:

        decision = controller.decide(signal)

        print(decision)


        if decision["decision"]["decision"] == "TRADE":

            opened = controller.execute(
                signal["symbol"],
                signal,
                50
            )

            print("\nOPEN:")
            print(opened)



    # -----------------------------
    # SIMULATE MARKET RESULTS
    # -----------------------------

    results = {
        "BTCUSDT": 120,
        "ETHUSDT": -50,
        "SOLUSDT": 80
    }


    print("\nCLOSING POSITIONS:")


    for symbol, pnl in results.items():

        position = controller.execution.positions[symbol][0]

        position["status"] = "CLOSED"
        position["realized_pnl"] = pnl
        position["exit"] = 55


        learning = controller.learn(position)

        print(symbol)
        print(learning)



    # -----------------------------
    # FINAL STATE
    # -----------------------------

    print("\nFINAL BRAIN:")
    print(controller.optimize())


    print("\nFINAL MEMORY:")
    print(controller.memory.history)


    controller.close()


    print("\nAUTONOMOUS MULTI POSITION PASSED ✅")



if __name__ == "__main__":
    run_test()
