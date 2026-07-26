from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_93AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManagerRuntimeSupervisorController:


    def __init__(self, supervisor):

        self.supervisor = supervisor

        self.controller_status = RuntimeStatus.INITIALIZED

        self.control_cycles = 0

        self.last_decision = None

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



    def start_controller(self):

        try:

            result = (
                self.supervisor.start_supervision()
            )


            self.controller_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "CONTROLLER_START",
                    "time": self._time()
                }
            )


            return {

                "controller_status":
                    self.controller_status.value,

                "supervisor":
                    result,

                "started_at":
                    self._time()
            }



        except Exception as error:

            self.controller_status = RuntimeStatus.ERROR

            return {

                "controller_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def control_supervision_cycle(self):

        self.control_cycles += 1


        try:

            supervision = (
                self.supervisor.supervise_runtime_cycle()
            )


            decision = supervision.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.control_history.append(
                {
                    "cycle": self.control_cycles,
                    "decision": decision,
                    "time": self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.controller_status = RuntimeStatus.ACTIVE

            else:

                self.controller_status = RuntimeStatus.ERROR



            return {

                "controller_status":
                    self.controller_status.value,

                "decision":
                    decision,

                "supervision":
                    supervision,

                "control_cycles":
                    self.control_cycles,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.controller_status = RuntimeStatus.ERROR

            return {

                "controller_status":
                    "ERROR",

                "decision":
                    DecisionStatus.BLOCK.value,

                "error":
                    str(error)
            }



    def health(self):

        return {

            "available":
                True,

            "controller_status":
                self.controller_status.value,

            "last_decision":
                self.last_decision,

            "control_cycles":
                self.control_cycles,

            "control_history_size":
                len(self.control_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_controller(self):

        try:

            result = (
                self.supervisor.recover_supervision()
            )


            self.controller_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "supervisor":
                    result,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.controller_status = RuntimeStatus.ERROR

            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop_controller(self):

        result = (
            self.supervisor.stop_supervision()
        )


        self.controller_status = RuntimeStatus.STOPPED


        return {

            "controller_status":
                self.controller_status.value,

            "supervisor":
                result,

            "stopped_at":
                self._time()
        }
