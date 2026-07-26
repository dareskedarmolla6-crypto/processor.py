from brain.performance_memory import PerformanceMemory
from brain.feedback_engine import FeedbackEngine
from brain.signal_pipeline import SignalPipeline
from brain.adaptive_brain import AdaptiveBrain
from brain.capital_allocator import CapitalAllocator
from risk.risk_manager import RiskGovernor
from brain.execution_engine import ExecutionEngine
from brain.smart_exit import SmartExit
from brain.risk_engine import RiskEngine
from brain.position_manager import PositionManager
from brain.autonomous_loop import AutonomousLoop


class MockStore:

    def __init__(self):
        self.data = {
            "system_status":"RUN"
        }

    def set(self,k,v):
        self.data[k]=v

    def get(self,k):
        return self.data.get(k)



def run_test():

    print(
        "========== AUTONOMOUS LEARNING LOOP TEST =========="
    )


    memory = PerformanceMemory()

    pipeline = SignalPipeline(
        memory
    )

    brain = AdaptiveBrain(
        memory
    )

    allocator = CapitalAllocator()


    governor = RiskGovernor(
        MockStore()
    )


    execution = ExecutionEngine()

    smart_exit = SmartExit()

    risk = RiskEngine(
        max_risk_per_trade=0.03
    )


    pm = PositionManager(
        execution,
        smart_exit,
        risk
    )


    feedback = FeedbackEngine(
        memory
    )


    loop = AutonomousLoop(
        pipeline,
        brain,
        allocator,
        governor,
        None,
        pm,
        feedback
    )


    market = [

        {
            "symbol":"BTCUSDT",
            "price":60000,
            "signal":"BUY",
            "confidence":0.90
        },

        {
            "symbol":"ETHUSDT",
            "price":3000,
            "signal":"BUY",
            "confidence":0.70
        }

    ]


    result = loop.run(
        market,
        1000
    )


    print("\nRESULT:")
    print(result)


    assert "trades" in result

    print(
        "\nAUTONOMOUS LEARNING LOOP PASSED ✅"
    )


if __name__=="__main__":
    run_test()
