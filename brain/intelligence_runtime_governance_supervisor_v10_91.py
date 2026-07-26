from datetime import datetime, UTC


class IntelligenceRuntimeGovernanceSupervisorV10_91:
    """
    FSE Intelligence Runtime Governance Supervisor V10.91

    Responsibilities
    ----------------
    - Supervise governance manager
    - Validate governance availability
    - Provide governance health status

    Does NOT contain
    ----------------
    - Learning logic
    - Decision logic
    - Execution logic
    """


    def __init__(
        self,
        governance_manager
    ):

        self.governance_manager = governance_manager



    def supervise(self):

        governance = (
            self.governance_manager.evaluate()
        )


        return {
            "status":
                "GOVERNANCE_ACTIVE"
                if governance["governance_status"] == "ACTIVE"
                else "GOVERNANCE_INACTIVE",

            "governance":
                governance,

            "checked_at":
                datetime.now(
                    UTC
                ).isoformat()
        }



    def health(self):

        health = (
            self.governance_manager.health()
        )


        return {
            "governance_available":
                health["governance_available"],

            "runtime_status":
                health["runtime_status"]
        }
