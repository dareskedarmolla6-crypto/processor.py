from brain.performance_memory import PerformanceMemory
from brain.autonomous_brain import AutonomousBrain
from brain.capital_allocator import CapitalAllocator
from risk.risk_manager import RiskGovernor
from brain.position_manager import PositionManager
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from brain.live_loop import LiveAutonomousLoop


class MockStore:

    def __init__(self):
        self.data = {
            "system_status": "RUN"
        }

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)



def run_test():

    print("========== LIVE LOOP TEST ==========")


    # Memory

    memory = PerformanceMemory()

    memory.record(
        "BTCUSDT",
        100
    )


    # Brain

    brain = AutonomousBrain(
        memory
    )


    # Capital

    allocator = CapitalAllocator()


    # Risk

    store = MockStore()

    governor = RiskGovernor(
        store
    )


    # Position

    position_manager = PositionManager(

        execution=ExecutionEngine(),

        smart_exit=SmartExit(),

        risk_engine=RiskEngine()

    )


    # Live Engine

    loop = LiveAutonomousLoop(

        brain=brain,

        allocator=allocator,

        governor=governor,

        position_manager=position_manager

    )



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
            "confidence": 0.65
        }

    ]



    result = loop.run_cycle(
        market,
        balance=1000
    )


    print("\nFINAL RESULT:")
    print(result)



    assert "trades" in result

    assert len(result["trades"]) > 0


    print(
        "\nLIVE LOOP TEST PASSED ✅"
    )



if __name__ == "__main__":
    run_test()
