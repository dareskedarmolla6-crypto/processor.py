from datetime import datetime, timezone


class IntelligenceRuntimeV11_92AutonomousRuntimeDecisionGovernanceExecutionOrchestrator:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }

    VALID_RUNTIME_STATUS = {
        "ACTIVE",
        "ERROR",
        "STOPPED",
        "INITIALIZED",
    }

    def __init__(self, execution_controller):

        self.execution_controller = execution_controller

        self.orchestrator_status = "INITIALIZED"
        self.runtime_status = "INITIALIZED"

        self.last_decision = None

        self.execution_cycles = 0

        self.started_at = None
        self.last_execution_at = None

        self.decision_history = []
        self.health_history = []
        self.lifecycle_events = []  # 👈 AttributeError እንዳይከሰት እዚህ ጋር ተጨምሯል

        self.runtime_statistics = {
            "successful_cycles": 0,
            "failed_cycles": 0,
            "blocked_cycles": 0,
            "allowed_cycles": 0,
        }

    def _time(self):
        return datetime.now(timezone.utc).isoformat()

    def validate_dependencies(self):

        dependency = {
            "controller_available": False,
            "health_available": False,
            "status": "FAILED",
            "dependency_status": "FAILED",  # 👈 ከ recover_runtime() ጋር እንዲጣጣም
            "checked_at": self._time(),
        }

        if self.execution_controller is None:
            return dependency

        dependency["controller_available"] = True

        if hasattr(self.execution_controller, "health"):
            dependency["health_available"] = True

        if hasattr(self.execution_controller, "control_execution_governance"):
            dependency["status"] = "ACTIVE"
            dependency["dependency_status"] = "READY"  # 👈 ከ "READY" ቼክ ጋር ለማጣጣም

        return dependency

    def start_runtime(self):

        dependency = self.validate_dependencies()

        if dependency["status"] != "ACTIVE":
            self.orchestrator_status = "ERROR"
            self.runtime_status = "ERROR"

            return {
                "runtime_status": "ERROR",
                "orchestrator_status": "ERROR",
                "dependency": dependency,
                "checked_at": self._time(),
            }

        self.started_at = self._time()

        self.orchestrator_status = "ACTIVE"
        self.runtime_status = "ACTIVE"

        return {
            "runtime_status": "ACTIVE",
            "orchestrator_status": "ACTIVE",
            "dependency": dependency,
            "started_at": self.started_at,
        }

    def orchestrate_execution(self):

        self.execution_cycles += 1

        record = {
            "cycle": self.execution_cycles,
            "started_at": self._time(),
        }

        try:
            if self.runtime_status != "ACTIVE":
                startup = self.start_runtime()
                if startup["runtime_status"] != "ACTIVE":
                    raise RuntimeError("Runtime startup failed.")

            controller_result = (
                self.execution_controller
                .control_execution_governance()
            )

            decision = controller_result.get(
                "decision",
                "BLOCK",
            )

            if decision not in self.VALID_DECISIONS:
                decision = "BLOCK"

            self.last_decision = decision
            self.last_execution_at = self._time()

            # የስታቲስቲክስ መዛግብት ማዘመኛ
            if decision == "ALLOW":
                self.runtime_statistics["allowed_cycles"] += 1
            else:
                self.runtime_statistics["blocked_cycles"] += 1
            self.runtime_statistics["successful_cycles"] += 1

            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()
            self.decision_history.append(record)

            # 🔄 የቴስቱን ኮንትራት የሚያረካ ሙሉ የሪተርን መዋቅር
            return {
                "orchestrator_status": self.orchestrator_status,
                "runtime_status": self.runtime_status,
                "decision": decision,
                "control": controller_result,
                "checked_at": self._time(),
            }

        except Exception as error:
            self.runtime_statistics["failed_cycles"] += 1
            record["status"] = "FAILED"
            record["error"] = str(error)
            self.decision_history.append(record)

            return {
                "orchestrator_status": "ERROR",
                "runtime_status": "ERROR",
                "decision": "BLOCK",
                "error": str(error),
                "checked_at": self._time(),
            }

    def aggregate_health(self):

        controller_health = None

        if hasattr(self.execution_controller, "health"):
            try:
                controller_health = (
                    self.execution_controller
                    .health()
                )
            except Exception as error:
                controller_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }

        return {
            "orchestrator_status": self.orchestrator_status,
            "runtime_status": self.runtime_status,
            "controller_health": controller_health,
            "checked_at": self._time(),
        }

    def health(self):

        return {
            "autonomous_runtime_decision_governance_execution_orchestrator_available": True,
            "orchestrator_status": self.orchestrator_status,
            "runtime_status": self.runtime_status,
            "last_decision": self.last_decision,
            "execution_cycles": self.execution_cycles,
            "decision_history_size": len(self.decision_history),
            "lifecycle_events": len(self.lifecycle_events),
            "aggregated_health": self.aggregate_health(),
            "checked_at": self._time(),
        }

    def stop_runtime(self):

        self.orchestrator_status = "STOPPED"
        self.runtime_status = "STOPPED"

        self.lifecycle_events.append(
            {
                "event": "RUNTIME_STOPPED",
                "timestamp": self._time(),
            }
        )

        return {
            "orchestrator_status": "STOPPED",
            "runtime_status": "STOPPED",
            "stopped_at": self._time(),
        }

    def recover_runtime(self):

        dependency_check = self.validate_dependencies()

        if dependency_check["dependency_status"] != "READY":
            self.orchestrator_status = "ERROR"
            self.runtime_status = "ERROR"

            return {
                "recovery_status": "FAILED",
                "runtime_status": "ERROR",
                "dependency": dependency_check,
                "checked_at": self._time(),
            }

        self.orchestrator_status = "ACTIVE"
        self.runtime_status = "ACTIVE"

        self.lifecycle_events.append(
            {
                "event": "RUNTIME_RECOVERED",
                "timestamp": self._time(),
            }
        )

        return {
            "recovery_status": "SUCCESS",
            "runtime_status": "ACTIVE",
            "checked_at": self._time(),
        }
