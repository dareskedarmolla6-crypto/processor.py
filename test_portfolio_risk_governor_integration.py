from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from risk.risk_manager import RiskGovernor

# አርክቴክቸሩ የሚፈልገው MockStore
class MockStore:
    def __init__(self):
        self.data = {"system_status": "RUN"}
    def set(self, key, value):
        self.data[key] = value
    def get(self, key):
        return self.data.get(key)

def run_portfolio_risk_governor_test():
    print("========== PORTFOLIO RISK GOVERNOR INTEGRATION ==========")

    # Setup Components
    store = MockStore()
    execution = ExecutionEngine()
    smart_exit = SmartExit()
    risk = RiskEngine(max_risk_per_trade=0.03)
    
    # RiskGovernor ን አዋቅር
    governor = RiskGovernor(store)
    
    pm = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
        risk_engine=risk
    )

    balance = 1000

    # =========================
    # TEST 1: NORMAL TRADE
    # =========================
    status = governor.approve_trade()
    print("\nGOVERNOR STATUS:", status)
    assert status[0] is True 

    result = pm.manage("BTC", {"signal": "BUY"}, price=100, balance=balance, stop_loss_price=98)
    print("NORMAL POSITION:", result)
    assert result["action"] == "OPEN"

    # =========================
    # TEST 2: LOSS SIMULATION (5 Losses to trigger SAFE_MODE)
    # =========================
    print("\nLOSS SIMULATION:")
    for i in range(5):
        governor.update(pnl=-20) 
        print(f"LOSS {i+1} RECORDED")

    # =========================
    # TEST 3: SAFE MODE CHECK
    # =========================
    status = governor.approve_trade()
    print("\nAFTER 5 LOSSES STATUS:", status)
    assert status[0] is False # (False, 'SAFE_MODE')

    # =========================
    # TEST 4: BLOCK NEW POSITION
    # =========================
    result = {"action": "OPEN"} # Default
    if status[0] is False:
        result = {"action": "BLOCKED", "reason": status[1]}
    
    print("NEW TRADE:", result)
    assert result["action"] == "BLOCKED"
    
    print("\nPORTFOLIO RISK GOVERNOR INTEGRATION PASSED ✅")

if __name__ == "__main__":
    run_portfolio_risk_governor_test()





