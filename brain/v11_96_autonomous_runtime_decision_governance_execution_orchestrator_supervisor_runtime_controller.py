from datetime import datetime, timezone


class IntelligenceRuntimeV11_96AutonomousRuntimeDecisionGovernanceExecutionOrchestratorSupervisorRuntimeController:


    def __init__(self, manager):

        self.manager = manager

        self.controller_status = "INITIALIZED"
        self.runtime_status = "INITIALIZED"

        self.last_decision = None

        self.control_cycles = 0

        self.control_history = []

        self.lifecycle_events = []



    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def start_controller(self):

        if self.manager is None:

            self.controller_status = "ERROR"
            self.runtime_status = "ERROR"

            return {

                "controller_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "reason":
                    "manager_missing",

                "checked_at":
                    self._time(),
            }



        if hasattr(
            self.manager,
            "start_manager"
        ):

            result = (
                self.manager
                .start_manager()
            )


            if (
                result.get(
                    "manager_status"
                )
                == "ACTIVE"
            ):

                self.controller_status = "ACTIVE"
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

                    "controller_status":
                        "ACTIVE",

                    "runtime_status":
                        "ACTIVE",

                    "management":
                        result,

                    "started_at":
                        self._time(),
                }



        self.controller_status = "ERROR"
        self.runtime_status = "ERROR"


        return {

            "controller_status":
                "ERROR",

            "runtime_status":
                "ERROR",

            "checked_at":
                self._time(),
        }



    def execute_control_cycle(self):

        self.control_cycles += 1


        if self.manager is None:

            self.controller_status = "ERROR"
            self.runtime_status = "ERROR"


            return {

                "controller_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "decision":
                    "BLOCK",

                "checked_at":
                    self._time(),
                }



        result = (
            self.manager
            .execute_management_cycle()
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
                "management_status"
            )
            == "ACTIVE"
        ):

            self.controller_status = "ACTIVE"
            self.runtime_status = "ACTIVE"


        else:

            self.controller_status = "ERROR"
            self.runtime_status = "ERROR"



        self.control_history.append(
            {
                "cycle":
                    self.control_cycles,

                "decision":
                    decision,

                "status":
                    self.controller_status,

                "checked_at":
                    self._time(),
            }
        )


        return {

            "controller_status":
                self.controller_status,

            "runtime_status":
                self.runtime_status,

            "decision":
                decision,

            "management":
                result,

            "control_cycles":
                self.control_cycles,

            "checked_at":
                self._time(),
        }


    def health(self):

        manager_health = None


        if hasattr(
            self.manager,
            "health"
        ):

            try:

                manager_health = (
                    self.manager.health()
                )

            except Exception as error:

                manager_health = {
                    "runtime_status":
                        "FAILED",

                    "error":
                        str(error),
                }



        return {

            "autonomous_runtime_decision_governance_execution_orchestrator_supervisor_runtime_controller_available":
                True,


            "controller_status":
                self.controller_status,


            "runtime_status":
                self.runtime_status,


            "last_decision":
                self.last_decision,


            "control_cycles":
                self.control_cycles,


            "control_history_size":
                len(
                    self.control_history
                ),


            "lifecycle_events":
                len(
                    self.lifecycle_events
                ),


            "manager_health":
                manager_health,


            "checked_at":
                self._time(),
        }



    def recover_controller(self):

        if self.manager is None:

            self.controller_status = "ERROR"
            self.runtime_status = "ERROR"


            return {

                "recovery_status":
                    "FAILED",

                "controller_status":
                    "ERROR",

                "runtime_status":
                    "ERROR",

                "checked_at":
                    self._time(),
            }



        if hasattr(
            self.manager,
            "recover_manager"
        ):

            recovery = (
                self.manager
                .recover_manager()
            )


            if (
                recovery.get(
                    "recovery_status"
                )
                == "SUCCESS"
            ):

                self.controller_status = "ACTIVE"
                self.runtime_status = "ACTIVE"


                return {

                    "recovery_status":
                        "SUCCESS",

                    "controller_status":
                        "ACTIVE",

                    "runtime_status":
                        "ACTIVE",

                    "checked_at":
                        self._time(),
                }



        self.controller_status = "ERROR"
        self.runtime_status = "ERROR"


        return {

            "recovery_status":
                "FAILED",

            "controller_status":
                "ERROR",

            "runtime_status":
                "ERROR",

            "checked_at":
                self._time(),
        }



    def stop_controller(self):

        self.controller_status = "STOPPED"
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

            "controller_status":
                "STOPPED",

            "runtime_status":
                "STOPPED",

            "stopped_at":
                self._time(),
        }
