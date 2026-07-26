from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import RuntimeStatus


class IntelligenceRuntimeV11_89AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorController:

    def __init__(self, health_supervisor):

        self.health_supervisor = health_supervisor

        self.controller_status = RuntimeStatus.INITIALIZED

        self.runtime_status = RuntimeStatus.INITIALIZED

        self.control_cycles = 0

        self.control_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start(self):

        try:

            self.runtime_status = RuntimeStatus.ACTIVE

            self.controller_status = RuntimeStatus.ACTIVE


            event = {

                "event":
                    "START",

                "checked_at":
                    self._time(),
            }


            self.lifecycle_events.append(
                event
            )


            return {

                "controller_status":
                    self.controller_status.value,

                "runtime_status":
                    self.runtime_status.value,

                "started_at":
                    self._time(),
            }



        except Exception as error:


            self.controller_status = RuntimeStatus.ERROR

            return {

                "controller_status":
                    RuntimeStatus.ERROR.value,

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def control_cycle(self):

        self.control_cycles += 1


        try:

            supervision = (
                self.health_supervisor
                .supervise_health()
            )


            decision = (
                supervision.get(
                    "decision"
                )
            )


            if (
                decision == "ALLOW"
                and supervision.get(
                    "supervisor_status"
                )
                == RuntimeStatus.ACTIVE.value
            ):

                self.controller_status = RuntimeStatus.ACTIVE
                self.runtime_status = RuntimeStatus.ACTIVE


            else:

                self.controller_status = RuntimeStatus.ERROR
                self.runtime_status = RuntimeStatus.ERROR



            record = {

                "cycle":
                    self.control_cycles,

                "decision":
                    decision,

                "controller_status":
                    self.controller_status.value,

                "checked_at":
                    self._time(),
            }


            self.control_history.append(
                record
            )


            return {

                "controller_status":
                    self.controller_status.value,

                "runtime_status":
                    self.runtime_status.value,

                "decision":
                    decision,

                "supervision":
                    supervision,

                "control_cycles":
                    self.control_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.controller_status = RuntimeStatus.ERROR
            self.runtime_status = RuntimeStatus.ERROR


            return {

                "controller_status":
                    RuntimeStatus.ERROR.value,

                "runtime_status":
                    RuntimeStatus.ERROR.value,

                "decision":
                    "BLOCK",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def health(self):

        return {

            "autonomous_runtime_decision_governance_manager_runtime_health_supervisor_controller_available":
                True,

            "controller_status":
                self.controller_status.value,

            "runtime_status":
                self.runtime_status.value,

            "control_cycles":
                self.control_cycles,

            "control_history_size":
                len(self.control_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time(),
        }



    def recover(self):

        try:

            recovery = (
                self.health_supervisor
                .recover()
            )


            if (
                recovery.get(
                    "recovery_status"
                )
                == "SUCCESS"
            ):

                self.controller_status = RuntimeStatus.ACTIVE
                self.runtime_status = RuntimeStatus.ACTIVE

            else:

                self.controller_status = RuntimeStatus.ERROR
                self.runtime_status = RuntimeStatus.ERROR



            return {

                "recovery_status":
                    recovery.get(
                        "recovery_status"
                    ),

                "controller_status":
                    self.controller_status.value,

                "runtime_status":
                    self.runtime_status.value,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def stop(self):

        self.runtime_status = RuntimeStatus.STOPPED

        self.controller_status = RuntimeStatus.STOPPED


        return {

            "controller_status":
                self.controller_status.value,

            "runtime_status":
                self.runtime_status.value,

            "stopped_at":
                self._time(),
        }
