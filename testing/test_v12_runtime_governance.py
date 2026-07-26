from brain.v12_autonomous_runtime_governance_foundation import (
    AutonomousRuntimeGovernanceFoundationV12
)


class MockSupervisor:

    def __init__(self):
        self.status = "READY"


    def health(self):

        return {
            "runtime_status": "ACTIVE"
        }


class MockController:

    def control_execution_governance(self):

        return {
            "decision": "ALLOW",
            "runtime_status": "ACTIVE"
        }


class MockOrchestrator:

    def orchestrate_execution(self):

        return {
            "decision": "ALLOW"
        }


class MockFullSystem:

    def run(
        self,
        symbol,
        balance,
        stop_loss_price=None
    ):

        return {
            "status": "EXECUTED",
            "symbol": symbol
        }



def create_runtime():

    return AutonomousRuntimeGovernanceFoundationV12(

        runtime_supervisor=MockSupervisor(),

        execution_controller=MockController(),

        orchestrator=MockOrchestrator(),

        full_system=MockFullSystem()
    )



def test_v12_runtime_start():

    runtime = create_runtime()

    result = runtime.start_runtime()

    assert result["runtime_status"] == "ACTIVE"



def test_v12_dependency_validation():

    runtime = create_runtime()

    result = runtime.validate_dependencies()

    assert result["ready"] is True



def test_v12_execution_cycle_allow():

    runtime = create_runtime()

    runtime.start_runtime()

    result = runtime.execute_cycle(
        symbol="BTCUSDT",
        balance=1000
    )

    assert result["decision"] == "ALLOW"



def test_v12_health():

    runtime = create_runtime()

    health = runtime.health()

    assert (
        health["v12_runtime_available"]
        if "v12_runtime_available" in health
        else
        health["autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_available"]
    )
