from datetime import datetime, timezone


class IntelligenceRuntimeV11_74AutonomousRuntimeGovernor:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }

    def __init__(self, runtime_supervisor):

        self.runtime_supervisor = runtime_supervisor
        self.governor_status = "INITIALIZED"
        self.last_decision = None
        self.governance_cycles = 0
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def govern_runtime(self):

        self.governance_cycles += 1

        record = {
            "cycle": self.governance_cycles,
            "started_at": self._time(),
        }

        try:

            supervision = (
                self.runtime_supervisor.supervise_runtime()
            )

            decision = supervision.get(
                "decision",
                "BLOCK"
            )


            if decision not in self.VALID_DECISIONS:
                decision = "BLOCK"


            self.last_decision = decision


            if decision == "ALLOW":
                self.governor_status = "ACTIVE"
            else:
                self.governor_status = "BLOCKED"


            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)


            return {
                "governor_status": self.governor_status,
                "runtime_status": (
                    "ACTIVE"
                    if self.governor_status == "ACTIVE"
                    else "ERROR"
                ),
                "decision": decision,
                "supervision": supervision,
                "governance_cycles": self.governance_cycles,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.governor_status = "ERROR"
            self.last_decision = "BLOCK"


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)


            return {
                "governor_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        dependency_health = None

        if hasattr(
            self.runtime_supervisor,
            "health"
        ):

            try:

                dependency_health = (
                    self.runtime_supervisor.health()
                )

            except Exception:

                dependency_health = {
                    "runtime_status": "FAILED"
                }


        return {

            "autonomous_runtime_governor_available": True,

            "governor_status":
                self.governor_status,

            "runtime_status":
                (
                    "ACTIVE"
                    if self.governor_status == "ACTIVE"
                    else "ERROR"
                ),

            "last_decision":
                self.last_decision,

            "governance_cycles":
                self.governance_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.governor_status = "STOPPED"

        return {
            "governor_status": "STOPPED",
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }
