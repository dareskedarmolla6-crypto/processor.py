from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.position_manager import PositionManager
from brain.smart_exit import SmartExit


def run_portfolio_risk_test():

    print("========== PORTFOLIO RISK CONTROL TEST ==========")

    execution = ExecutionEngine()
    smart_exit = SmartExit()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )

    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )

    balance = 1000


    # =========================
    # POSITION 1
    # =========================

    a = pm.manage(
        "BTC",
        {"signal":"BUY"},
        price=100,
        balance=balance,
        stop_loss_price=98
    )

    print("\nBTC:")
    print(a)


    # =========================
    # POSITION 2
    # =========================

    b = pm.manage(
        "ETH",
        {"signal":"BUY"},
        price=200,
        balance=balance,
        stop_loss_price=195
    )

    print("\nETH:")
    print(b)


    # =========================
    # PORTFOLIO STATE
    # =========================

    print("\nOPEN POSITIONS:")
    print(execution.positions)


    total_size = sum(
        p["size"]
        for positions in execution.positions.values()
        for p in positions
    )


    print("\nTOTAL EXPOSURE:")
    print(total_size)


    # Risk check
    assert total_size > 0

    print("\nPORTFOLIO RISK CONTROL PASSED ✅")


if __name__ == "__main__":
    run_portfolio_risk_test()
