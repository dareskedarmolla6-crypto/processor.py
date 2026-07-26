from datetime import datetime, timezone


class IntelligenceRuntimeV11_95AutonomousRuntimeDecisionGovernanceExecutionOrchestratorSupervisorRuntimeManager:


    def __init__(self, runtime):

        self.runtime = runtime

        self.manager_status = "INITIALIZED"
        self.runtime_status = "INITIALIZED"

        self.last_decision = None

        self.management_cycles = 0

        self.management_history = []

        self.lifecycle_events = []



    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def start_manager(self):

        if self.runtime is None:

            self.manager_status = "ERROR"
            self.runtime_status = "ERROR"

            return {

                "manager_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "reason":
                    "runtime_missing",

                "checked_at":
                    self._time(),
            }



        if hasattr(
            self.runtime,
            "start_runtime"
        ):

            result = (
                self.runtime
                .start_runtime()
            )


            if (
                result.get(
                    "runtime_status"
                )
                == "ACTIVE"
            ):

                self.manager_status = "ACTIVE"
                self.runtime_status = "ACTIVE"


                self.lifecycle_events.append(
                    {
                        "event":
                            "START",

                        "status":
                            "ACTIVE",

                        "checked_at":
                            self._time(),
                    }
                )


                return {

                    "manager_status":
                        "ACTIVE",

                    "runtime_status":
                        "ACTIVE",

                    "runtime":
                        result,

                    "started_at":
                        self._time(),
                }



        self.manager_status = "ERROR"
        self.runtime_status = "ERROR"


        return {

            "manager_status":
                "ERROR",

                "runtime_status":
                    "ERROR",

                "checked_at":
                    self._time(),
        }



    def execute_management_cycle(self):

        self.management_cycles += 1


        if self.runtime is None:

            self.manager_status = "ERROR"
            self.runtime_status = "ERROR"

            return {

                "management_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "decision":
                    "BLOCK",

                "checked_at":
                    self._time(),
            }



        result = (
            self.runtime
            .execute_supervision_cycle()
        )


        decision = result.get(
            "decision"
        )


        if decision not in {
            "ALLOW",
            "BLOCK",
        }:

            decision = "BLOCK"



        self.last_decision = decision


        if (
            result.get(
                "runtime_status"
            )
            == "ACTIVE"
        ):

            self.manager_status = "ACTIVE"
            self.runtime_status = "ACTIVE"


        else:

            self.manager_status = "ERROR"
            self.runtime_status = "ERROR"



        self.management_history.append(
            {
                "cycle":
                    self.management_cycles,

                "decision":
                    decision,

                "status":
                    self.manager_status,

                "checked_at":
                    self._time(),
            }
        )


        return {

            "management_status":
                self.manager_status,

            "runtime_status":
                self.runtime_status,

            "decision":
                decision,

            "runtime":
                result,

            "management_cycles":
                self.management_cycles,

            "checked_at":
                self._time(),
        }


    def health(self):

        runtime_health = None


        if hasattr(
            self.runtime,
            "health"
        ):

            try:

                runtime_health = (
                    self.runtime.health()
                )

            except Exception as error:

                runtime_health = {

                    "runtime_status":
                        "FAILED",

                    "error":
                        str(error),
                }



        return {

            "autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_manager_available":
                True,


            "manager_status":
                self.manager_status,


            "runtime_status":
                self.runtime_status,


            "last_decision":
                self.last_decision,


            "management_cycles":
                self.management_cycles,


            "management_history_size":
                len(
                    self.management_history
                ),


            "lifecycle_events":
                len(
                    self.lifecycle_events
                ),


            "runtime_health":
                runtime_health,


            "checked_at":
                self._time(),
        }



    def recover_manager(self):

        if self.runtime is None:

            self.manager_status = "ERROR"
            self.runtime_status = "ERROR"


            return {

                "recovery_status":
                    "FAILED",

                "manager_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "checked_at":
                    self._time(),
            }



        if hasattr(
            self.runtime,
            "recover_runtime"
        ):

            recovery = (
                self.runtime
                .recover_runtime()
            )


            if (
                recovery.get(
                    "recovery_status"
                )
                == "SUCCESS"
            ):

                self.manager_status = "ACTIVE"
                self.runtime_status = "ACTIVE"


                return {

                    "recovery_status":
                        "SUCCESS",

                    "manager_status":
                        "ACTIVE",

                    "runtime_status":
                        "ACTIVE",

                    "checked_at":
                        self._time(),
                }



        self.manager_status = "ERROR"
        self.runtime_status = "ERROR"


        return {

            "recovery_status":
                "FAILED",

            "manager_status":
                "ERROR",

            "runtime_status":
                "ERROR",

            "checked_at":
                self._time(),
        }



    def stop_manager(self):

        self.manager_status = "STOPPED"
        self.runtime_status = "STOPPED"


        self.lifecycle_events.append(
            {
                "event":
                    "STOP",

                "status":
                    "STOPPED",

                "checked_at":
                    self._time(),
            }
        )


        return {

            "manager_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
