from datetime import datetime, timezone


class IntelligenceRuntimeV11_76GovernanceRuntimeController:

    def __init__(self, governance):

        self.governance = governance
        self.runtime_status = "STOPPED"
        self.last_error = None
        self.started_at = None


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def start(self):

        self.runtime_status = "ACTIVE"
        self.started_at = self._time()
        self.last_error = None

        return {
            "runtime_status": "ACTIVE",
            "started_at": self.started_at,
        }


    def execute_governance(self):

        try:

            result = (
                self.governance.govern_runtime()
            )

            if (
                result["governance_status"]
                == "FAILED"
            ):

                self.runtime_status = "ERROR"
                self.last_error = (
                    result.get("error")
                    or "Governance execution failure"
                )

                return {
                    "controller_status": "FAILED",
                    "runtime_status": "ERROR",
                    "error": self.last_error,
                    "checked_at": self._time(),
                }


            self.runtime_status = "ACTIVE"

            return {
                "controller_status": "ACTIVE",
                "runtime_status": self.runtime_status,
                "governance": result,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.runtime_status = "ERROR"
            self.last_error = str(error)

            return {
                "controller_status": "FAILED",
                "runtime_status": "ERROR",
                "error": str(error),
                "checked_at": self._time(),
            }


    def stop(self):

        self.runtime_status = "STOPPED"

        return {
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }


    def health(self):

        try:

            dependency_health = (
                self.governance.health()
            )


        except Exception as error:

            dependency_health = {
                "runtime_status": "FAILED",
                "error": str(error),
            }


            return {
                "governance_runtime_controller_available": True,
                "runtime_status": self.runtime_status,
                "last_error": self.last_error,
                "dependency_health": dependency_health,
                "checked_at": self._time(),
            }


        return {
            "governance_runtime_controller_available": True,
            "runtime_status": self.runtime_status,
            "last_error": self.last_error,
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }
