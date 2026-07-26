from datetime import datetime, timezone


class IntelligenceRuntimeV11_90AutonomousRuntimeDecisionGovernanceExecutionManager:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(self, execution_coordinator):

        self.execution_coordinator = execution_coordinator

        self.manager_status = "INITIALIZED"
        self.last_decision = None

        self.management_cycles = 0
        self.decision_history = []



    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def manage_execution_governance(self):

        self.management_cycles += 1


        record = {
            "cycle": self.management_cycles,
            "started_at": self._time(),
        }


        try:

            coordination = (
                self.execution_coordinator
                .coordinate_execution_governance()
            )


            decision = coordination.get(
                "decision"
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"



            self.last_decision = decision



            if (
                coordination.get("coordination_status")
                == "ACTIVE"
                and decision == "ALLOW"
            ):

                self.manager_status = "ACTIVE"

            else:

                self.manager_status = "ERROR"



            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)



            return {

                "management_status":
                    self.manager_status,

                "runtime_status":
                    "ACTIVE"
                    if self.manager_status == "ACTIVE"
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


            self.manager_status = "ERROR"
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
            self.execution_coordinator,
            "health"
        ):

            try:

                dependency_health = (
                    self.execution_coordinator.health()
                )


            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }



        return {

            "autonomous_runtime_decision_governance_execution_manager_available":
                True,

            "manager_status":
                self.manager_status,

            "runtime_status":
                "ACTIVE"
                if self.manager_status == "ACTIVE"
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

        self.manager_status = "STOPPED"


        return {

            "manager_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
