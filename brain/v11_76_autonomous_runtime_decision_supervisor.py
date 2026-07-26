from datetime import datetime, timezone


class IntelligenceRuntimeV11_76AutonomousRuntimeDecisionSupervisor:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }

    def __init__(self, decision_engine):
        self.decision_engine = decision_engine
        self.supervisor_status = "INITIALIZED"
        self.last_decision = None
        self.supervision_cycles = 0
        self.decision_history = []

    def _time(self):
        return datetime.now(timezone.utc).isoformat()

    def supervise_decision(self):

        self.supervision_cycles += 1

        record = {
            "cycle": self.supervision_cycles,
            "started_at": self._time(),
        }

        try:
            decision_result = (
                self.decision_engine.evaluate_decision()
            )

            decision = decision_result.get(
                "decision"
            )

            if decision not in self.VALID_DECISIONS:
                decision = "BLOCK"

            self.last_decision = decision

            if decision == "ALLOW":
                self.supervisor_status = "ACTIVE"
            else:
                self.supervisor_status = "BLOCKED"

            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)

            return {
                "supervision_status": "ACTIVE",
                "runtime_status": (
                    "ACTIVE"
                    if decision == "ALLOW"
                    else "ERROR"
                ),
                "decision": decision,
                "engine": decision_result,
                "supervision_cycles": self.supervision_cycles,
                "checked_at": self._time(),
            }

        except Exception as error:

            self.supervisor_status = "ERROR"
            self.last_decision = "BLOCK"

            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)

            return {
                "supervision_status": "FAILED",
                "runtime_status": "ERROR",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }


    def health(self):

        dependency_health = None

        if hasattr(
            self.decision_engine,
            "health"
        ):
            try:
                dependency_health = (
                    self.decision_engine.health()
                )

            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }


        return {
            "autonomous_runtime_decision_supervisor_available": True,
            "supervisor_status": self.supervisor_status,
            "runtime_status": (
                "ACTIVE"
                if self.supervisor_status == "ACTIVE"
                else "ERROR"
            ),
            "last_decision": self.last_decision,
            "supervision_cycles": self.supervision_cycles,
            "decision_history_size": len(
                self.decision_history
            ),
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }


    def stop(self):

        self.supervisor_status = "STOPPED"

        return {
            "supervisor_status": "STOPPED",
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }
