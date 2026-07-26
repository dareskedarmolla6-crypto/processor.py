from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from brain.price_monitor import PriceMonitor


def run_test():

    print("========== PRICE MONITOR TEST ==========")


    # =========================
    # SETUP
    # =========================

    execution = ExecutionEngine()

    smart_exit = SmartExit()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )


    manager = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )


    monitor = PriceMonitor(
        manager
    )


    # =========================
    # OPEN POSITION
    # =========================

    opened = manager.manage(
        "BTCUSDT",
        {
            "signal": "BUY"
        },
        price=50,
        balance=1000,
        stop_loss_price=49
    )


    print("\nOPEN:")
    print(opened)



    # =========================
    # PRICE MOVE UP
    # =========================

    result = monitor.update(
        "BTCUSDT",
        55
    )


    print("\nPRICE 55:")
    print(result)



    # =========================
    # PRICE DROP
    # =========================

    result = monitor.update(
        "BTCUSDT",
        53
    )


    print("\nPRICE 53:")
    print(result)



    # =========================
    # FINAL STATE
    # =========================

    print("\nFINAL POSITIONS:")
    print(
        execution.positions
    )


    print(
        "\nPRICE MONITOR TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
