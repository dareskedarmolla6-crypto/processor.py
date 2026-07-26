from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_91AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManagerRuntime:


    def __init__(self, manager):

        self.manager = manager

        self.runtime_status = RuntimeStatus.INITIALIZED

        self.runtime_cycles = 0

        self.last_decision = None

        self.runtime_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start_runtime(self):

        try:

            result = self.manager.start()

            self.runtime_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "RUNTIME_START",
                    "time": self._time()
                }
            )


            return {

                "runtime_status":
                    self.runtime_status.value,

                "manager":
                    result,

                "started_at":
                    self._time()
            }


        except Exception as error:

            self.runtime_status = RuntimeStatus.ERROR

            return {

                "runtime_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def execute_runtime_cycle(self):

        self.runtime_cycles += 1


        try:

            management = (
                self.manager.manage_cycle()
            )


            decision = management.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.runtime_history.append(
                {
                    "cycle": self.runtime_cycles,
                    "decision": decision,
                    "time": self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.runtime_status = RuntimeStatus.ACTIVE

            else:

                self.runtime_status = RuntimeStatus.ERROR



            return {

                "runtime_status":
                    self.runtime_status.value,

                "decision":
                    decision,

                "management":
                    management,

                "runtime_cycles":
                    self.runtime_cycles,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.runtime_status = RuntimeStatus.ERROR

            return {

                "runtime_status":
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

            "runtime_status":
                self.runtime_status.value,

            "last_decision":
                self.last_decision,

            "runtime_cycles":
                self.runtime_cycles,

            "runtime_history_size":
                len(self.runtime_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_runtime(self):

        try:

            result = self.manager.recover()


            self.runtime_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "manager":
                    result,

                "checked_at":
                    self._time()
            }


        except Exception as error:

            self.runtime_status = RuntimeStatus.ERROR

            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop_runtime(self):

        result = self.manager.stop()


        self.runtime_status = RuntimeStatus.STOPPED


        return {

            "runtime_status":
                self.runtime_status.value,

            "manager":
                result,

            "stopped_at":
                self._time()
        }
