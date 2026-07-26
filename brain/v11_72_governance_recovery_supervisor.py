from datetime import datetime, timezone


class IntelligenceRuntimeV11_72GovernanceRecoverySupervisor:

    def __init__(self, controller):

        self.controller = controller
        self.supervision_status = "INITIALIZED"
        self.last_status = None


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def supervise_runtime(self):

        try:

            health = (
                self.controller.health()
            )


            if (
                health["runtime_status"]
                == "ERROR"
            ):

                self.supervision_status = "ERROR"
                self.last_status = "FAILURE_DETECTED"

                return {
                    "supervision_status": "ERROR",
                    "decision": "RECOVERY_REQUIRED",
                    "runtime_health": health,
                    "checked_at": self._time(),
                }


            self.supervision_status = "ACTIVE"
            self.last_status = "HEALTHY"

            return {
                "supervision_status": "ACTIVE",
                "decision": "NO_ACTION",
                "runtime_health": health,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.supervision_status = "ERROR"
            self.last_status = "FAILED"

            return {
                "supervision_status": "FAILED",
                "runtime_status": "ERROR",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        try:

            dependency_health = (
                self.controller.health()
            )


        except Exception as error:

            dependency_health = {
                "runtime_status": "FAILED",
                "error": str(error),
            }


            return {
                "governance_recovery_supervisor_available": True,
                "supervision_status": "ERROR",
                "last_status": self.last_status,
                "dependency_health": dependency_health,
                "checked_at": self._time(),
            }


        return {
            "governance_recovery_supervisor_available": True,
            "supervision_status": self.supervision_status,
            "last_status": self.last_status,
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }
