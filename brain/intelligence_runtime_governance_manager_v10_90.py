from datetime import datetime, UTC


class IntelligenceRuntimeGovernanceManagerV10_90:
    """
    FSE Intelligence Runtime Governance Manager V10.90

    Responsibilities
    ----------------
    - Manage runtime governance state
    - Aggregate control supervision
    - Provide governance status

    Does NOT contain
    ----------------
    - Learning logic
    - Decision logic
    - Execution logic
    """


    def __init__(
        self,
        control_supervisor
    ):

        self.control_supervisor = control_supervisor



    def evaluate(self):

        supervision = (
            self.control_supervisor.supervise()
        )

        health = (
            self.control_supervisor.health()
        )


        return {
            "governance_status":
                "ACTIVE"
                if supervision["status"] == "CONTROL_ACTIVE"
                else "INACTIVE",

            "control_status":
                supervision,

            "health":
                health,

            "checked_at":
                datetime.now(
                    UTC
                ).isoformat()
        }



    def health(self):

        health = (
            self.control_supervisor.health()
        )


        return {
            "governance_available":
                health["control_available"],

            "runtime_status":
                health["runtime_status"]
        }
