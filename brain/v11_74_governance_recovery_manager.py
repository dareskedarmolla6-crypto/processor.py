from datetime import datetime, timezone


class IntelligenceRuntimeV11_74GovernanceRecoveryManager:

    def __init__(self, coordinator):

        self.coordinator = coordinator
        self.management_status = "INITIALIZED"
        self.last_management = None


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def manage_recovery(self):

        try:

            result = (
                self.coordinator.coordinate_recovery()
            )


            if (
                result["coordination_status"]
                == "FAILED"
            ):

                self.management_status = "ERROR"
                self.last_management = "FAILED"

                return {
                    "management_status": "FAILED",
                    "runtime_status": "ERROR",
                    "decision": "FAILED",
                    "coordination": result,
                    "checked_at": self._time(),
                }


            self.management_status = "ACTIVE"
            self.last_management = (
                result.get("decision")
            )


            return {
                "management_status": "ACTIVE",
                "decision": result.get("decision"),
                "coordination": result,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.management_status = "ERROR"
            self.last_management = "FAILED"

            return {
                "management_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "FAILED",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        try:

            dependency_health = (
                self.coordinator.health()
            )


        except Exception as error:

            dependency_health = {
                "runtime_status": "FAILED",
                "error": str(error),
            }


            return {
                "governance_recovery_manager_available": True,
                "management_status": "ERROR",
                "last_management": self.last_management,
                "dependency_health": dependency_health,
                "checked_at": self._time(),
            }


        return {
            "governance_recovery_manager_available": True,
            "management_status": self.management_status,
            "last_management": self.last_management,
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }
