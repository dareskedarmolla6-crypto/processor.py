from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit


def run_test():

    print("========== GLOBAL RISK GATE TEST ==========")

    execution = ExecutionEngine()
    risk = RiskEngine(max_risk_per_trade=0.03)

    pm = PositionManager(
        execution=execution,
        smart_exit=SmartExit(),
        risk_engine=risk
    )

    balance = 1000


    # Existing huge exposure
    execution.positions["BIG"] = [
        {
            "id":99,
            "side":"LONG",
            "size":600,
            "status":"OPEN"
        }
    ]


    result = pm.manage(
        "COIN_NEW",
        {"signal":"BUY"},
        price=50,
        balance=balance,
        stop_loss_price=49
    )

    print("\nRESULT:")
    print(result)


    assert result["action"] == "BLOCKED"

    print("\nGLOBAL RISK GATE PASSED ✅")


if __name__ == "__main__":
    run_test()
