from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit


def run_multi_position_test():

    print("========== MULTI POSITION RISK TEST ==========")

    execution = ExecutionEngine()
    smart_exit = SmartExit()

    risk = RiskEngine(
        max_drawdown=30,
        max_leverage=40,
        max_risk_per_trade=0.03
    )

    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )


    # ==========================
    # POSITION 1
    # ==========================
    result1 = pm.manage(
        "COIN_A",
        {"signal": "BUY"},
        price=100,
        balance=1000,
        stop_loss_price=98
    )

    print("\nCOIN_A:", result1)


    # ==========================
    # POSITION 2
    # ==========================
    result2 = pm.manage(
        "COIN_B",
        {"signal": "SELL"},
        price=200,
        balance=1000,
        stop_loss_price=204
    )

    print("\nCOIN_B:", result2)


    # ==========================
    # POSITION 3
    # ==========================
    result3 = pm.manage(
        "COIN_C",
        {"signal": "BUY"},
        price=50,
        balance=1000,
        stop_loss_price=49
    )

    print("\nCOIN_C:", result3)


    print("\nALL POSITIONS:")
    print(execution.positions)


    # Validation
    assert "COIN_A" in execution.positions
    assert "COIN_B" in execution.positions
    assert "COIN_C" in execution.positions


    for symbol, positions in execution.positions.items():
        assert positions[0]["status"] == "OPEN"


    print("\nMULTI POSITION TEST PASSED ✅")


if __name__ == "__main__":
    run_multi_position_test()
