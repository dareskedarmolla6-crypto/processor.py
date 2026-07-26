from brain.performance_memory import PerformanceMemory
from brain.signal_pipeline import SignalPipeline
from brain.capital_allocator import CapitalAllocator

from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine

from risk.risk_manager import RiskGovernor


class MockStore:

    def __init__(self):
        self.data = {
            "system_status": "RUN"
        }

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)



def run_brain_execution_cycle():

    print("========== BRAIN EXECUTION CYCLE TEST ==========")


    # =========================
    # MEMORY + BRAIN
    # =========================

    memory = PerformanceMemory()

    # Learning history
    memory.record("BTCUSDT", 100)
    memory.record("BTCUSDT", 50)

    memory.record("ETHUSDT", -20)
    memory.record("ETHUSDT", -30)


    pipeline = SignalPipeline(memory)


    market = [

        {
            "symbol": "BTCUSDT",
            "price": 60000,
            "signal": "BUY",
            "confidence": 0.75
        },

        {
            "symbol": "ETHUSDT",
            "price": 3000,
            "signal": "BUY",
            "confidence": 0.75
        },

        {
            "symbol": "SOLUSDT",
            "price": 150,
            "signal": "SELL",
            "confidence": 0.80
        }

    ]


    signals = pipeline.process(market)


    print("\nBRAIN DECISIONS:")

    for s in signals:
        print(s)


    # =========================
    # CAPITAL ALLOCATION
    # =========================

    allocator = CapitalAllocator()


    opportunities = [

        x for x in signals
        if x["decision"] == "TRADE"

    ]


    allocations = allocator.allocate(
        balance=1000,
        opportunities=opportunities
    )


    print("\nALLOCATIONS:")
    print(allocations)


    # =========================
    # RISK GOVERNOR
    # =========================

    store = MockStore()

    governor = RiskGovernor(store)


    status = governor.approve_trade()


    print("\nRISK GOVERNOR:")
    print(status)


    assert status[0] is True


    # =========================
    # EXECUTION LAYER
    # =========================

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


    for signal in opportunities:

        symbol = signal["symbol"]

        print(
            f"\nEXECUTING {symbol}"
        )


        result = pm.manage(
            symbol,
            {
                "signal": signal["signal"]
            },
            price=market[
                [
                    x["symbol"]
                    for x in market
                ].index(symbol)
            ]["price"],
            balance=balance,
            stop_loss_price=
            market[
                [
                    x["symbol"]
                    for x in market
                ].index(symbol)
            ]["price"] * 0.98
        )


        print(result)

        assert result["action"] == "OPEN"



    print("\nFINAL POSITIONS:")
    print(execution.positions)


    print(
        "\nBRAIN EXECUTION CYCLE PASSED ✅"
    )



if __name__ == "__main__":
    run_brain_execution_cycle()
