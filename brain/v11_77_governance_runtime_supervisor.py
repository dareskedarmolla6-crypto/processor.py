from datetime import datetime, timezone


class IntelligenceRuntimeV11_77GovernanceRuntimeSupervisor:

    VALID_DECISIONS = {
        "NO_ACTION",
        "RECOVERY_REQUIRED",
        "FAILED",
    }


    def __init__(self, controller):

        self.controller = controller
        self.supervision_status = "INITIALIZED"
        self.last_decision = None
        self.last_checked_at = None
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def _record_decision(self, decision):

        timestamp = self._time()

        self.last_decision = decision
        self.last_checked_at = timestamp

        self.decision_history.append(
            {
                "decision": decision,
                "checked_at": timestamp,
            }
        )


    def supervise_runtime(self):

        try:

            health = self.controller.health()

            runtime_status = (
                health.get("runtime_status")
            )


            if runtime_status == "ERROR":

                self.supervision_status = "ERROR"

                self._record_decision(
                    "RECOVERY_REQUIRED"
                )

                return {
                    "supervision_status": "ERROR",
                    "decision": "RECOVERY_REQUIRED",
                    "runtime_health": health,
                    "checked_at": self._time(),
                }


            if runtime_status != "ACTIVE":

                self.supervision_status = "WARNING"

                self._record_decision(
                    "RECOVERY_REQUIRED"
                )

                return {
                    "supervision_status": "WARNING",
                    "decision": "RECOVERY_REQUIRED",
                    "runtime_health": health,
                    "checked_at": self._time(),
                }


            self.supervision_status = "ACTIVE"

            self._record_decision(
                "NO_ACTION"
            )


            return {
                "supervision_status": "ACTIVE",
                "decision": "NO_ACTION",
                "runtime_health": health,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.supervision_status = "ERROR"

            self._record_decision(
                "FAILED"
            )


            return {
                "supervision_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "FAILED",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        try:

            dependency_health = (
                self.controller.health()
            )

            available = True


        except Exception as error:

            dependency_health = {
                "runtime_status": "FAILED",
                "error": str(error),
            }

            available = False


        return {

            "governance_runtime_supervisor_available":
                available,

            "supervision_status":
                self.supervision_status,

            "last_decision":
                self.last_decision,

            "last_checked_at":
                self.last_checked_at,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }
