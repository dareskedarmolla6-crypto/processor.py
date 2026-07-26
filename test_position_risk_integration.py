from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit

def run_position_risk_integration():

    print("========== POSITION + RISK INTEGRATION TEST ==========")

    # =========================
    # SETUP
    # =========================
    execution = ExecutionEngine()
    smart_exit = SmartExit()

    # RiskEngine ን በተገቢው parameter አዋቅር
    risk = RiskEngine(max_risk_per_trade=0.03)

    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )

    balance = 1000

    # =========================
    # TEST 1: SAFE POSITION OPEN
    # =========================
    result = pm.manage(
        "COIN_SAFE",
        {"signal": "BUY"},
        price=100,
        balance=balance,
        stop_loss_price=98
    )

    print("\nSAFE OPEN:")
    print(result)

    assert result["action"] == "OPEN"

    # =========================
    # TEST 2: INVALID STOP LOSS
    # =========================
    # Stop loss ከዋጋ ጋር እኩል ከሆነ size 0 ስለሚሆን INVALID_PARAMS ይመለሳል
    result = pm.manage(
        "COIN_INVALID",
        {"signal": "BUY"},
        price=100,
        balance=balance,
        stop_loss_price=100
    )

    print("\nINVALID STOP LOSS:")
    print(result)

    # የ PositionManager ምላሽ ትክክል መሆኑን እናረጋግጥ
    assert result["position"] == "INVALID_PARAMS"

    # =========================
    # TEST 3: EXISTING POSITION MANAGEMENT
    # =========================
    result = pm.manage(
        "COIN_SAFE",
        {"signal": "BUY"},
        price=110
    )

    print("\nPROFIT MANAGEMENT:")
    print(result)

    assert result["action"] in [
        "LOCK_PROFIT",
        "PARTIAL_CLOSE",
        "HOLD"
    ]

    # =========================
    # FINAL STATE
    # =========================
    print("\nOPEN POSITIONS:")
    print(execution.positions)

    print("\nPOSITION + RISK INTEGRATION PASSED ✅")

if __name__ == "__main__":
    run_position_risk_integration()
