from datetime import datetime, timezone


class IntelligenceRuntimeV11_81AutonomousRuntimeDecisionGovernanceController:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(self, governance_manager):

        self.governance_manager = governance_manager

        self.controller_status = "INITIALIZED"
        self.last_decision = None

        self.control_cycles = 0
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def control_decision_governance(self):

        self.control_cycles += 1

        record = {
            "cycle": self.control_cycles,
            "started_at": self._time(),
        }


        try:

            management = (
                self.governance_manager
                .manage_decision_governance()
            )


            decision = management.get(
                "decision"
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"


            self.last_decision = decision


            if decision == "ALLOW":

                self.controller_status = "ACTIVE"

            else:

                self.controller_status = "BLOCKED"



            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)



            return {

                "controller_status":
                    self.controller_status,

                "runtime_status":
                    "ACTIVE"
                    if self.controller_status == "ACTIVE"
                    else "ERROR",

                "decision":
                    decision,

                "management":
                    management,

                "control_cycles":
                    self.control_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.controller_status = "ERROR"
            self.last_decision = "BLOCK"


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)



            return {

                "controller_status":
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
            self.governance_manager,
            "health"
        ):

            try:

                dependency_health = (
                    self.governance_manager.health()
                )

            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }



        return {

            "autonomous_runtime_decision_governance_controller_available":
                True,

            "controller_status":
                self.controller_status,

            "runtime_status":
                "ACTIVE"
                if self.controller_status == "ACTIVE"
                else "ERROR",

            "last_decision":
                self.last_decision,

            "control_cycles":
                self.control_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.controller_status = "STOPPED"

        return {

            "controller_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
