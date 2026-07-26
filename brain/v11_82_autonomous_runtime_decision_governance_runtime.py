from datetime import datetime, timezone


class IntelligenceRuntimeV11_82AutonomousRuntimeDecisionGovernanceRuntime:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(self, governance_controller):

        self.governance_controller = governance_controller

        self.runtime_status = "INITIALIZED"
        self.last_decision = None

        self.runtime_cycles = 0
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def execute_runtime_governance(self):

        self.runtime_cycles += 1

        record = {
            "cycle": self.runtime_cycles,
            "started_at": self._time(),
        }


        try:

            control = (
                self.governance_controller
                .control_decision_governance()
            )


            decision = control.get(
                "decision"
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"


            self.last_decision = decision


            if (
                control.get("controller_status")
                == "ACTIVE"
                and decision == "ALLOW"
            ):

                self.runtime_status = "ACTIVE"

            else:

                self.runtime_status = "ERROR"



            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)



            return {

                "runtime_status":
                    self.runtime_status,

                "decision":
                    decision,

                "control":
                    control,

                "runtime_cycles":
                    self.runtime_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:

            self.runtime_status = "ERROR"
            self.last_decision = "BLOCK"


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)



            return {

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
            self.governance_controller,
            "health"
        ):

            try:

                dependency_health = (
                    self.governance_controller.health()
                )

            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }



        return {

            "autonomous_runtime_decision_governance_runtime_available":
                True,

            "runtime_status":
                self.runtime_status,

            "last_decision":
                self.last_decision,

            "runtime_cycles":
                self.runtime_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.runtime_status = "STOPPED"

        return {

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
