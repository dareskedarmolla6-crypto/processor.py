from datetime import datetime, timezone


class IntelligenceRuntimeV11_72AutonomousRuntimeControl:

    VALID_ACTIONS = {
        "ALLOW",
        "BLOCK",
    }

    def __init__(self, runtime_governance):
        self.runtime_governance = runtime_governance
        self.control_status = "INITIALIZED"
        self.last_action = None
        self.control_cycles = 0
        self.action_history = []

    def _time(self):
        return datetime.now(timezone.utc).isoformat()

    def control_runtime(self):
        self.control_cycles += 1

        record = {
            "cycle": self.control_cycles,
            "started_at": self._time(),
        }

        try:
            governance = (
                self.runtime_governance.evaluate_runtime()
            )

            decision = governance.get(
                "decision"
            )

            if decision not in self.VALID_ACTIONS:
                decision = "BLOCK"

            self.last_action = decision

            if decision == "ALLOW":
                self.control_status = "ACTIVE"
            else:
                self.control_status = "BLOCKED"

            record["action"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.action_history.append(record)

            # 🔄 የተጠናከረው የ ACTIVE ኮንትራት (ከ 'action' እና 'decision' ጋር)
            return {
                "control_status": self.control_status,
                "runtime_status": "ACTIVE" if self.control_status == "ACTIVE" else "ERROR",
                "action": decision,
                "decision": decision,
                "governance": governance,
                "control_cycles": self.control_cycles,
                "checked_at": self._time(),
            }

        except Exception as error:
            self.control_status = "ERROR"
            self.last_action = "BLOCK"

            record["status"] = "FAILED"
            record["error"] = str(error)

            self.action_history.append(record)

            # 🔄 የተጠናከረው የ FAILED ኮንትራት (ከ 'action' እና 'decision' ጋር)
            return {
                "control_status": "FAILED",
                "runtime_status": "ERROR",
                "action": "BLOCK",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }

    # 🔄 የተስተካከለው የሄልዝ ኮንትራት (Health Contract)
    def health(self):
        dependency_health = None

        if hasattr(self.runtime_governance, "health"):
            try:
                dependency_health = (
                    self.runtime_governance.health()
                )
            except Exception:
                dependency_health = {
                    "runtime_status": "FAILED"
                }

        return {
            "autonomous_runtime_control_available": True,
            "control_status": self.control_status,
            "runtime_status": (
                "ACTIVE"
                if self.control_status == "ACTIVE"
                else "ERROR"
            ),
            "last_action": self.last_action,
            "control_cycles": self.control_cycles,
            "action_history_size": len(
                self.action_history
            ),
            "dependency_health": dependency_health,
            "checked_at": self._time(),
        }

    def stop(self):
        self.control_status = "STOPPED"
        return {
            "control_status": self.control_status,
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }
