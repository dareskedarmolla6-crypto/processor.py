from datetime import datetime, timezone


class IntelligenceRuntimeV11_71GovernanceRuntimeController:

    def __init__(self, manager):

        self.manager = manager
        self.runtime_status = "INITIALIZED"
        self.started_at = None
        self.stopped_at = None
        self.last_error = None


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def start(self):

        self.runtime_status = "ACTIVE"
        self.started_at = self._time()

        return {
            "runtime_status": self.runtime_status,
            "started_at": self.started_at,
        }


    def execute_management(self):

        try:

            result = (
                self.manager.manage_governance()
            )

            if (
                result["management_status"]
                == "FAILED"
            ):

                self.runtime_status = "ERROR"
                self.last_error = (
                    result.get("error")
                )

                return {
                    "controller_status": "FAILED",
                    "runtime_status": "ERROR",
                    "management": result,
                    "checked_at": self._time(),
                }


            self.runtime_status = "ACTIVE"

            return {
                "controller_status": "ACTIVE",
                "runtime_status": "ACTIVE",
                "management": result,
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
                "governance_runtime_controller_available": True,
                "runtime_status": "ERROR",
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



    def stop(self):

        self.runtime_status = "STOPPED"
        self.stopped_at = self._time()

        return {
            "runtime_status": self.runtime_status,
            "stopped_at": self.stopped_at,
        }
