from datetime import datetime, timezone


class IntelligenceRuntimeV11_75GovernanceRuntimeGovernance:

    def __init__(self, manager):

        self.manager = manager
        self.governance_status = "INITIALIZED"
        self.last_decision = None


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def govern_runtime(self):

        try:

            result = (
                self.manager.manage_recovery()
            )


            if (
                result["management_status"]
                == "FAILED"
            ):

                self.governance_status = "ERROR"
                self.last_decision = "FAILED"

                return {
                    "governance_status": "FAILED",
                    "runtime_status": "ERROR",
                    "decision": "FAILED",
                    "management": result,
                    "checked_at": self._time(),
                }


            self.governance_status = "ACTIVE"
            self.last_decision = (
                result.get("decision")
            )

            return {
                "governance_status": "ACTIVE",
                "decision": self.last_decision,
                "management": result,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.governance_status = "ERROR"
            self.last_decision = "FAILED"

            return {
                "governance_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "FAILED",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        try:

            dependency_health = (
                self.manager.health()
            )


        except Exception as error:

            dependency_health = {
                "runtime_status": "FAILED",
                "error": str(error),
            }


            return {
                "governance_runtime_available": True,
                "governance_status": "ERROR",
                "last_decision": self.last_decision,
                "dependency_health": dependency_health,
                "checked_at": self._time(),
            }


        return {
            "governance_runtime_available": True,
            "governance_status": self.governance_status,
            "last_decision": self.last_decision,
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }
