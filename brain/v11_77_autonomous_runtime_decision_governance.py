from datetime import datetime, timezone


class IntelligenceRuntimeV11_77AutonomousRuntimeDecisionGovernance:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }

    def __init__(self, decision_supervisor):

        self.decision_supervisor = decision_supervisor
        self.governance_status = "INITIALIZED"
        self.last_decision = None
        self.governance_cycles = 0
        self.decision_history = []

    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def govern_runtime_decision(self):

        self.governance_cycles += 1

        record = {
            "cycle": self.governance_cycles,
            "started_at": self._time(),
        }

        try:

            supervision = (
                self.decision_supervisor.supervise_decision()
            )

            decision = supervision.get(
                "decision"
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"


            self.last_decision = decision


            if decision == "ALLOW":

                self.governance_status = "ACTIVE"

            else:

                self.governance_status = "BLOCKED"


            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)


            return {
                "governance_status": self.governance_status,
                "runtime_status": (
                    "ACTIVE"
                    if decision == "ALLOW"
                    else "ERROR"
                ),
                "decision": decision,
                "supervision": supervision,
                "governance_cycles": self.governance_cycles,
                "checked_at": self._time(),
            }


        except Exception as error:

            self.governance_status = "ERROR"
            self.last_decision = "BLOCK"


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)


            return {
                "governance_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }



    def health(self):

        dependency_health = None


        if hasattr(
            self.decision_supervisor,
            "health"
        ):

            try:

                dependency_health = (
                    self.decision_supervisor.health()
                )

            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }


        return {

            "autonomous_runtime_decision_governance_available": True,
            "governance_status": self.governance_status,
            "runtime_status": (
                "ACTIVE"
                if self.governance_status == "ACTIVE"
                else "ERROR"
            ),
            "last_decision": self.last_decision,
            "governance_cycles": self.governance_cycles,
            "decision_history_size": len(
                self.decision_history
            ),
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }



    def stop(self):

        self.governance_status = "STOPPED"

        return {
            "governance_status": "STOPPED",
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }
