from datetime import datetime, timezone


class IntelligenceRuntimeV11_87AutonomousRuntimeDecisionGovernanceExecutionRuntime:

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(self, controller_runtime):

        self.controller_runtime = controller_runtime

        self.execution_status = "INITIALIZED"
        self.last_decision = None

        self.execution_cycles = 0
        self.decision_history = []



    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def execute_runtime_governance(self):

        self.execution_cycles += 1


        record = {
            "cycle": self.execution_cycles,
            "started_at": self._time(),
        }


        try:

            control = (
                self.controller_runtime
                .control_runtime_governance()
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

                self.execution_status = "ACTIVE"

            else:

                self.execution_status = "ERROR"



            record["decision"] = decision
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)



            return {

                "execution_status":
                    self.execution_status,

                "runtime_status":
                    "ACTIVE"
                    if self.execution_status == "ACTIVE"
                    else "ERROR",

                "decision":
                    decision,

                "control":
                    control,

                "execution_cycles":
                    self.execution_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.execution_status = "ERROR"
            self.last_decision = "BLOCK"


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)



            return {

                "execution_status":
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
            self.controller_runtime,
            "health"
        ):

            try:

                dependency_health = (
                    self.controller_runtime.health()
                )


            except Exception as error:

                dependency_health = {
                    "runtime_status": "FAILED",
                    "error": str(error),
                }



        return {

            "autonomous_runtime_decision_governance_execution_runtime_available":
                True,

            "execution_status":
                self.execution_status,

            "runtime_status":
                "ACTIVE"
                if self.execution_status == "ACTIVE"
                else "ERROR",

            "last_decision":
                self.last_decision,

            "execution_cycles":
                self.execution_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.execution_status = "STOPPED"


        return {

            "execution_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
