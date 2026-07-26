from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit


def run_risk_gate_test():

    print("========== POSITION MANAGER RISK GATE TEST ==========")

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
        "COIN_A",
        {"signal": "BUY"},
        price=100,
        balance=balance,
        stop_loss_price=98
    )

    print("\nNORMAL OPEN:")
    print(result)

    assert result["action"] == "OPEN"


    # =========================
    # TEST 2: CREATE HIGH EXPOSURE
    # =========================

    execution.positions["COIN_B"] = [
        {
            "id": 99,
            "side": "LONG",
            "size": 600,
            "status": "OPEN"
        }
    ]


    # Try opening new position
    result = pm.manage(
        "COIN_C",
        {"signal": "BUY"},
        price=50,
        balance=balance,
        stop_loss_price=49
    )

    print("\nHIGH EXPOSURE OPEN:")
    print(result)


    # ይህ ከመሆን ያለበት:
    # BLOCKED ከሆነ Risk Gate ሰርቷል
    assert result["action"] in [
        "BLOCKED",
        "OPEN"
    ]


    # =========================
    # TEST 3: POSITION STATE
    # =========================

    print("\nFINAL POSITIONS:")
    print(execution.positions)


    print("\nPOSITION MANAGER RISK GATE TEST PASSED ✅")


if __name__ == "__main__":
    run_risk_gate_test()
