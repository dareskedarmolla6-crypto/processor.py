from brain.performance_memory import PerformanceMemory
from brain.autonomous_brain import AutonomousBrain
from brain.capital_allocator import CapitalAllocator
from risk.risk_manager import RiskGovernor
from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine

class MockStore:
    def __init__(self):
        self.data = {"system_status": "RUN"}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

def run_test():
    print("========== FULL AUTONOMOUS SYSTEM TEST ==========")

    # -------------------------
    # MEMORY + BRAIN
    # -------------------------
    memory = PerformanceMemory()
    memory.record("BTCUSDT", 100)
    memory.record("BTCUSDT", 50)

    brain = AutonomousBrain(memory)

    signals = [
        {"symbol": "BTCUSDT", "price": 60000, "signal": "BUY", "confidence": 0.75},
        {"symbol": "ETHUSDT", "price": 3000, "signal": "BUY", "confidence": 0.75}
    ]

    brain_result = brain.run_cycle(signals)
    print("\nBRAIN:")
    print(brain_result)

    # -------------------------
    # CAPITAL ALLOCATION
    # -------------------------
    allocator = CapitalAllocator()
    opportunities = [x for x in brain_result["decisions"] if x["decision"] == "TRADE"]

    allocations = allocator.allocate(
        1000,
        [{"symbol": x["symbol"], "confidence": x["confidence"]} for x in opportunities]
    )

    print("\nALLOCATIONS:")
    print(allocations)

    # -------------------------
    # RISK GOVERNOR
    # -------------------------
    store = MockStore()
    governor = RiskGovernor(store)
    status = governor.approve_trade()

    print("\nGOVERNOR:")
    print(status)
    assert status[0] is True

    # -------------------------
    # PORTFOLIO EXECUTION
    # -------------------------
    execution_engine = ExecutionEngine()
    risk_engine = RiskEngine()
    smart_exit = SmartExit()

    pm = PositionManager(
        execution=execution_engine,
        smart_exit=smart_exit,
        risk_engine=risk_engine
    )

    trades = []

    # የተስተካከለው የሎፕ አወቃቀር
    for item in allocations:
        if item["allocation"] <= 0:
            continue

        trade = pm.manage(
            item["symbol"],
            {"signal": "BUY"},
            price=60000,
            balance=1000,
            stop_loss_price=58000
        )

        trades.append({
            "symbol": item["symbol"],
            "trade": trade
        })

    print("\nTRADES:")
    print(trades)
    print("\nFULL AUTONOMOUS SYSTEM TEST PASSED ✅")

if __name__ == "__main__":
    run_test()
