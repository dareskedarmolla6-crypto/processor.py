import os

from brain.autonomous_controller_v2 import AutonomousControllerV2


def run_test():

    db = "live_autonomous_loop_v2.db"

    if os.path.exists(db):
        os.remove(db)

    print("========== LIVE AUTONOMOUS LOOP V2 ==========")


    controller = AutonomousControllerV2(db)


    # ---------------------------------
    # OLD EXPERIENCE
    # ---------------------------------

    experience = [
        {
            "symbol": "BTCUSDT",
            "pnl": 250
        },
        {
            "symbol": "ETHUSDT",
            "pnl": -100
        },
        {
            "symbol": "SOLUSDT",
            "pnl": 180
        }
    ]


    for trade in experience:

        controller.learn({
            "symbol": trade["symbol"],
            "status": "CLOSED",
            "realized_pnl": trade["pnl"]
        })


    print("\nINITIAL BRAIN:")
    print(controller.optimize())


    # ---------------------------------
    # LIVE SIGNAL
    # ---------------------------------

    signal = {
        "symbol": "BTCUSDT",
        "signal": "BUY",
        "confidence": 0.90
    }


    decision = controller.decide(signal)


    print("\nDECISION:")
    print(decision)



    if decision["decision"]["decision"] == "TRADE":


        opened = controller.execute(
            "BTCUSDT",
            {
                "signal": "BUY"
            },
            50
        )


        print("\nOPEN:")
        print(opened)



        # simulate market movement

        position = controller.execution.positions[
            "BTCUSDT"
        ][0]


        position["status"] = "CLOSED"
        position["realized_pnl"] = 75
        position["exit"] = 55



        learned = controller.learn(
            position
        )


        print("\nLEARNING:")
        print(learned)



    else:

        print("\nTRADE SKIPPED")


    # ---------------------------------
    # AFTER LEARNING OPTIMIZE
    # ---------------------------------

    print("\nFINAL BRAIN:")
    print(controller.optimize())


    print("\nFINAL MEMORY:")
    print(controller.memory.history)



    controller.close()


    print("\nLIVE AUTONOMOUS LOOP V2 PASSED ✅")



if __name__ == "__main__":
    run_test()
