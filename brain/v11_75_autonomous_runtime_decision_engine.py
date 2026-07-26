from datetime import datetime, timezone


class IntelligenceRuntimeV11_75AutonomousRuntimeDecisionEngine:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }

    def __init__(self, runtime_governor):

        self.runtime_governor = runtime_governor
        self.engine_status = "INITIALIZED"
        self.last_decision = None
        self.decision_cycles = 0
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def evaluate_decision(self):

        self.decision_cycles += 1

        record = {
            "cycle": self.decision_cycles,
            "started_at": self._time(),
        }

        try:

            governance = (
                self.runtime_governor.govern_runtime()
            )

            decision = governance.get(
                "decision",
                "BLOCK"
            )


            if decision not in self.VALID_DECISIONS:
                decision = "BLOCK"


            self.last_decision = decision


            if decision == "ALLOW":
                self.engine_status = "ACTIVE"
            else:
                self.engine_status = "BLOCKED"


            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)


            return {
                "engine_status": self.engine_status,
                "runtime_status": (
                    "ACTIVE"
                    if self.engine_status == "ACTIVE"
                    else "ERROR"
                ),
                "decision": decision,
                "governance": governance,
                "decision_cycles": self.decision_cycles,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.engine_status = "ERROR"
            self.last_decision = "BLOCK"

            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)


            return {
                "engine_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        dependency_health = None

        if hasattr(
            self.runtime_governor,
            "health"
        ):

            try:

                dependency_health = (
                    self.runtime_governor.health()
                )

            except Exception:

                dependency_health = {
                    "runtime_status": "FAILED"
                }


        return {

            "autonomous_runtime_decision_engine_available": True,

            "engine_status":
                self.engine_status,

            "runtime_status":
                (
                    "ACTIVE"
                    if self.engine_status == "ACTIVE"
                    else "ERROR"
                ),

            "last_decision":
                self.last_decision,

            "decision_cycles":
                self.decision_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.engine_status = "STOPPED"

        return {
            "engine_status": "STOPPED",
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }
