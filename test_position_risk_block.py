from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit


def run_risk_block_test():

    print("========== POSITION RISK BLOCK TEST ==========")

    execution = ExecutionEngine()
    smart_exit = SmartExit()

    risk = RiskEngine(
        max_risk_per_trade=0.03,
        max_drawdown=30,
        max_leverage=40
    )

    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )

    balance = 1000


    # =========================
    # TEST 1: NORMAL OPEN
    # =========================

    result = pm.manage(
        "COIN_SAFE",
        {"signal": "BUY"},
        price=100,
        balance=balance,
        stop_loss_price=98
    )

    print("\nNORMAL:")
    print(result)

    assert result["action"] == "OPEN"


    # =========================
    # TEST 2: EMERGENCY STOP
    # =========================

    stopped = risk.emergency_stop(40)

    print("\nEMERGENCY:")
    print(stopped)

    assert stopped is True


    # =========================
    # TEST 3: EXPOSURE BLOCK
    # =========================

    open_positions = [
        {
            "size":600
        }
    ]

    check = risk.check_trade(
        balance=balance,
        position_size=50,
        open_positions=open_positions
    )

    print("\nEXPOSURE:")
    print(check)

    assert check == "BLOCKED"


    print("\nPOSITION RISK BLOCK TEST PASSED ✅")


if __name__ == "__main__":
    run_risk_block_test()
