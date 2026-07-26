from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_90AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManager:


    def __init__(self, controller):

        self.controller = controller

        self.manager_status = RuntimeStatus.INITIALIZED

        self.control_cycles = 0

        self.control_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )

        self.last_decision = None



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start(self):

        try:

            result = self.controller.start()

            self.manager_status = RuntimeStatus.ACTIVE

            self.lifecycle_events.append(
                {
                    "event": "START",
                    "time": self._time()
                }
            )


            return {

                "manager_status":
                    self.manager_status.value,

                "controller":
                    result,

                "started_at":
                    self._time()
            }


        except Exception as error:

            self.manager_status = RuntimeStatus.ERROR

            return {

                "manager_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def manage_cycle(self):

        self.control_cycles += 1


        try:

            control = self.controller.control_cycle()


            decision = control.get(
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


            return {

                "manager_status":
                    self.manager_status.value,

                "decision":
                    decision,

                "control":
                    control,

                "cycles":
                    self.control_cycles,

                "checked_at":
                    self._time()
            }


        except Exception as error:

            self.manager_status = RuntimeStatus.ERROR

            return {

                "manager_status":
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

            "manager_status":
                self.manager_status.value,

            "last_decision":
                self.last_decision,

            "control_cycles":
                self.control_cycles,

            "history_size":
                len(self.control_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover(self):

        try:

            result = self.controller.recover()

            self.manager_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "controller":
                    result,

                "checked_at":
                    self._time()
            }


        except Exception as error:

            self.manager_status = RuntimeStatus.ERROR

            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop(self):

        result = self.controller.stop()

        self.manager_status = RuntimeStatus.STOPPED


        return {

            "manager_status":
                self.manager_status.value,

            "controller":
                result,

            "stopped_at":
                self._time()
        }
