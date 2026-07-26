from brain.position_manager import PositionManager
from brain.risk_engine import RiskEngine
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit

def run_lifecycle_test():
    print("========== POSITION LIFECYCLE TEST ==========")

    # 1. Setup Engines
    execution = ExecutionEngine()
    smart_exit = SmartExit()
    risk = RiskEngine(max_risk_per_trade=0.03)
    pm = PositionManager(execution=execution, smart_exit=smart_exit, risk_engine=risk)

    # =========================
    # TEST 1: OPEN POSITION
    # =========================
    result = pm.manage("COIN_C", {"signal": "BUY"}, price=50, balance=1000, stop_loss_price=49)
    print("OPEN:", result)
    assert result["action"] == "OPEN"
    assert result["position"]["size"] == 30.0

    # =========================
    # TEST 2: LOCK PROFIT
    # =========================
    result = pm.manage("COIN_C", {"signal": "BUY"}, price=55)
    print("LOCK:", result)
    assert result["action"] == "LOCK_PROFIT"

    # =========================
    # TEST 3: REVERSAL
    # =========================
    # LONG ክፍት እያለ SELL ሲመጣ REVERSAL መሆን አለበት
    result = pm.manage("COIN_C", {"signal": "SELL"}, price=55)
    print("REVERSAL:", result)
    assert result["action"] == "REVERSAL"
    # የ REVERSAL መጠን የድሮውን 30.0 መያዝ አለበት
    assert result["position"]["size"] == 30.0

    # =========================
    # TEST 4: TRAILING STOP / PARTIAL EXIT
    # =========================
    # ዋጋው ከ 55 ወደ 50 ሲወርድ ቦቱ ወይ ሙሉ ለሙሉ ይወጣል ወይ በከፊል ይዘጋል
    result = pm.manage("COIN_C", {"signal": "SELL"}, price=50)
    print("TRAIL:", result)
    
    # የቦቱን ብልህነት (EXIT ወይም PARTIAL_CLOSE) እናረጋግጥ
    assert result["action"] in ["EXIT", "PARTIAL_CLOSE"]

    print("\nLifecycle Test Passed ✅")

if __name__ == "__main__":
    run_lifecycle_test()
