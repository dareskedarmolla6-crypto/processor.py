from datetime import datetime, UTC


class IntelligenceRuntimeGovernanceDecisionControlSupervisorV11_31:
    """
    FSE Intelligence Runtime Governance
    Decision Control Supervisor V11.31

    Responsibilities
    ----------------
    - Supervise decision control manager
    - Monitor control lifecycle
    - Expose control supervisor health

    Does NOT contain
    ----------------
    - Policy logic
    - Decision calculation
    - Execution logic
    """

    def __init__(self, decision_control_manager):

        self.decision_control_manager = (
            decision_control_manager
        )

    def supervise(self):

        control = (
            self.decision_control_manager.control()
        )

        health = (
            self.decision_control_manager.health()
        )

        return {
            "supervision_status":
                "ACTIVE"
                if control["control_status"]
                == "ACTIVE"
                else "INACTIVE",

            "control": control,

            "health": health,

            "checked_at":
                datetime.now(UTC).isoformat(),
        }

    def health(self):

        health = (
            self.decision_control_manager.health()
        )

        return {
            "decision_control_supervisor_available": True,

            "decision_control_manager_available":
                health[
                    "decision_control_manager_available"
                ],

            "runtime_status":
                health["runtime_status"],
        }
