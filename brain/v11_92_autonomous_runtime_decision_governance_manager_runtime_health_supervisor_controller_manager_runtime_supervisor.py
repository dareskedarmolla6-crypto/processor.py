from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_92AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManagerRuntimeSupervisor:


    def __init__(self, runtime):

        self.runtime = runtime

        self.supervisor_status = RuntimeStatus.INITIALIZED

        self.supervision_cycles = 0

        self.last_decision = None

        self.supervision_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start_supervision(self):

        try:

            runtime_status = (
                self.runtime.start_runtime()
            )


            self.supervisor_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "SUPERVISION_START",
                    "time": self._time()
                }
            )


            return {

                "supervisor_status":
                    self.supervisor_status.value,

                "runtime":
                    runtime_status,

                "started_at":
                    self._time()
            }



        except Exception as error:

            self.supervisor_status = RuntimeStatus.ERROR

            return {

                "supervisor_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def supervise_runtime_cycle(self):

        self.supervision_cycles += 1


        try:

            runtime_result = (
                self.runtime.execute_runtime_cycle()
            )


            decision = runtime_result.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.supervision_history.append(
                {
                    "cycle": self.supervision_cycles,
                    "decision": decision,
                    "time": self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.supervisor_status = RuntimeStatus.ACTIVE

            else:

                self.supervisor_status = RuntimeStatus.ERROR



            return {

                "supervisor_status":
                    self.supervisor_status.value,

                "decision":
                    decision,

                "runtime":
                    runtime_result,

                "supervision_cycles":
                    self.supervision_cycles,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.supervisor_status = RuntimeStatus.ERROR

            return {

                "supervisor_status":
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

            "supervisor_status":
                self.supervisor_status.value,

            "last_decision":
                self.last_decision,

            "supervision_cycles":
                self.supervision_cycles,

            "supervision_history_size":
                len(self.supervision_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_supervision(self):

        try:

            result = (
                self.runtime.recover_runtime()
            )


            self.supervisor_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "runtime":
                    result,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.supervisor_status = RuntimeStatus.ERROR


            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop_supervision(self):

        result = (
            self.runtime.stop_runtime()
        )


        self.supervisor_status = RuntimeStatus.STOPPED


        return {

            "supervisor_status":
                self.supervisor_status.value,

            "runtime":
                result,

            "stopped_at":
                self._time()
        }
