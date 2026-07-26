from datetime import datetime, timezone


class IntelligenceRuntimeV11_80AutonomousRuntimeDecisionGovernanceManager:

    def __init__(self, governance_coordinator):

        self.governance_coordinator = governance_coordinator

        self.management_status = "INITIALIZED"
        self.last_decision = None

        self.management_cycles = 0
        self.decision_history = []

    def _time(self):
        return datetime.now(timezone.utc).isoformat()


    def manage_decision_governance(self):

        self.management_cycles += 1

        record = {
            "cycle": self.management_cycles,
            "started_at": self._time(),
        }

        try:

            coordination = (
                self.governance_coordinator
                .coordinate_decision_governance()
            )


            decision = coordination.get(
                "decision"
            )


            if decision not in {
                "ALLOW",
                "BLOCK",
            }:
                decision = "BLOCK"


            self.last_decision = decision


            if coordination.get(
                "coordination_status"
            ) == "ACTIVE":

                self.management_status = "ACTIVE"

            else:

                self.management_status = "ERROR"


            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)


            return {

                "management_status":
                    self.management_status,

                "runtime_status":
                    "ACTIVE"
                    if self.management_status == "ACTIVE"
                    else "ERROR",

                "decision":
                    decision,

                "coordination":
                    coordination,

                "management_cycles":
                    self.management_cycles,

                "checked_at":
                    self._time(),
            }


        except Exception as error:

            self.management_status = "ERROR"
            self.last_decision = "BLOCK"

            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)


            return {

                "management_status":
                    "FAILED",

                "runtime_status":
                    "ERROR",

                "decision":
                    "BLOCK",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }


    def health(self):

        dependency_health = None


        if hasattr(
            self.governance_coordinator,
            "health"
        ):

            try:

                dependency_health = (
                    self.governance_coordinator.health()
                )

            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }


        return {

            "autonomous_runtime_decision_governance_manager_available":
                True,

            "management_status":
                self.management_status,

            "runtime_status":
                "ACTIVE"
                if self.management_status == "ACTIVE"
                else "ERROR",

            "last_decision":
                self.last_decision,

            "management_cycles":
                self.management_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }


    def stop(self):

        self.management_status = "STOPPED"

        return {

            "management_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
