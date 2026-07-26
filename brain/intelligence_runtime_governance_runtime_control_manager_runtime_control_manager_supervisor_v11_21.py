from datetime import datetime, UTC


class IntelligenceRuntimeGovernanceRuntimeControlManagerRuntimeControlManagerSupervisorV11_21:
    """
    FSE Intelligence Runtime Governance Runtime Control Manager
    Runtime Control Manager Supervisor V11.21
    """

    def __init__(self, runtime_control_orchestrator_manager):
        self.runtime_control_orchestrator_manager = (
            runtime_control_orchestrator_manager
        )

    def supervise(self):

        orchestration = (
            self.runtime_control_orchestrator_manager.orchestrate()
        )

        health = (
            self.runtime_control_orchestrator_manager.health()
        )

        return {
            "supervision_status": (
                "ACTIVE"
                if orchestration["orchestration_status"] == "ACTIVE"
                else "INACTIVE"
            ),
            "orchestration": orchestration,
            "health": health,
            "checked_at": datetime.now(UTC).isoformat(),
        }

    def health(self):

        health = (
            self.runtime_control_orchestrator_manager.health()
        )

        return {
            "runtime_control_manager_supervisor_available": True,
            "runtime_control_orchestrator_manager_available": health[
                "runtime_control_orchestrator_manager_available"
            ],
            "runtime_status": health["runtime_status"],
        }
