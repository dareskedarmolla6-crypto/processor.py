from datetime import datetime, timezone


class IntelligenceRuntimeV11_93AutonomousRuntimeDecisionGovernanceExecutionOrchestratorSupervisor:


    def __init__(self, orchestrator):

        self.orchestrator = orchestrator

        self.supervisor_status = "INITIALIZED"
        self.runtime_status = "INITIALIZED"

        self.last_decision = None

        self.supervision_cycles = 0

        self.supervision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def validate_orchestrator(self):

        if self.orchestrator is None:

            return {
                "status": "FAILED",
                "reason": "orchestrator_missing",
                "checked_at": self._time(),
            }


        if not hasattr(
            self.orchestrator,
            "health"
        ):

            return {
                "status": "FAILED",
                "reason": "invalid_orchestrator",
                "checked_at": self._time(),
            }


        return {
            "status": "READY",
            "dependency": "execution_orchestrator",
            "checked_at": self._time(),
        }



    def supervise_runtime(self):

        self.supervision_cycles += 1


        validation = (
            self.validate_orchestrator()
        )


        if validation["status"] != "READY":

            self.supervisor_status = "ERROR"
            self.runtime_status = "ERROR"


            return {

                "supervisor_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "reason":
                    validation,

                "checked_at":
                    self._time(),
            }


        health = (
            self.orchestrator.health()
        )


        decision = health.get(
            "last_decision"
        )


        if decision is None:

            decision = "BLOCK"



        self.last_decision = decision


        if (
            health.get("runtime_status")
            == "ACTIVE"
        ):

            self.supervisor_status = "ACTIVE"
            self.runtime_status = "ACTIVE"


        else:

            self.supervisor_status = "ERROR"
            self.runtime_status = "ERROR"



        record = {

            "cycle":
                self.supervision_cycles,

            "decision":
                decision,

            "status":
                self.supervisor_status,

            "checked_at":
                self._time(),
        }


        self.supervision_history.append(
            record
        )


        return {

            "supervisor_status":
                self.supervisor_status,

            "runtime_status":
                self.runtime_status,

            "decision":
                decision,

            "orchestrator_health":
                health,

            "supervision_cycles":
                self.supervision_cycles,

            "checked_at":
                self._time(),
        }


    def health(self):

        orchestrator_health = None


        if hasattr(
            self.orchestrator,
            "health"
        ):

            try:

                orchestrator_health = (
                    self.orchestrator.health()
                )

            except Exception as error:

                orchestrator_health = {

                    "runtime_status":
                        "FAILED",

                    "error":
                        str(error),
                }



        return {

            "autonomous_runtime_decision_governance_execution_orchestrator_supervisor_available":
                True,


            "supervisor_status":
                self.supervisor_status,


            "runtime_status":
                self.runtime_status,


            "last_decision":
                self.last_decision,


            "supervision_cycles":
                self.supervision_cycles,


            "supervision_history_size":
                len(
                    self.supervision_history
                ),


            "orchestrator_health":
                orchestrator_health,


            "checked_at":
                self._time(),
        }



    def recover_runtime(self):

        validation = (
            self.validate_orchestrator()
        )


        if validation["status"] != "READY":

            self.supervisor_status = "ERROR"

            self.runtime_status = "ERROR"


            return {

                "recovery_status":
                    "FAILED",

                "runtime_status":
                    "ERROR",

                "reason":
                    validation,

                "checked_at":
                    self._time(),
            }



        if hasattr(
            self.orchestrator,
            "recover_runtime"
        ):

            recovery = (
                self.orchestrator
                .recover_runtime()
            )


            if (
                recovery.get(
                    "recovery_status"
                )
                == "SUCCESS"
            ):

                self.supervisor_status = "ACTIVE"

                self.runtime_status = "ACTIVE"


                return {

                    "recovery_status":
                        "SUCCESS",

                    "runtime_status":
                        "ACTIVE",

                    "checked_at":
                        self._time(),
                }



        self.supervisor_status = "ERROR"

        self.runtime_status = "ERROR"


        return {

            "recovery_status":
                "FAILED",

            "runtime_status":
                "ERROR",

            "checked_at":
                self._time(),
        }



    def stop(self):

        self.supervisor_status = "STOPPED"

        self.runtime_status = "STOPPED"


        return {

            "supervisor_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
