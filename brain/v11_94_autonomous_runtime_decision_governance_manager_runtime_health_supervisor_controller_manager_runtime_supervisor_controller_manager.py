from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_94AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManagerRuntimeSupervisorControllerManager:


    def __init__(self, controller):

        self.controller = controller

        self.manager_status = RuntimeStatus.INITIALIZED

        self.management_cycles = 0

        self.last_decision = None

        self.management_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start_manager(self):

        try:

            result = (
                self.controller.start_controller()
            )

            self.manager_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "MANAGER_START",
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



    def manage_control_cycle(self):

        self.management_cycles += 1


        try:

            control = (
                self.controller.control_supervision_cycle()
            )


            decision = control.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.management_history.append(
                {
                    "cycle": self.management_cycles,
                    "decision": decision,
                    "time": self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.manager_status = RuntimeStatus.ACTIVE

            else:

                self.manager_status = RuntimeStatus.ERROR



            return {

                "manager_status":
                    self.manager_status.value,

                "decision":
                    decision,

                "control":
                    control,

                "management_cycles":
                    self.management_cycles,

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

            "management_cycles":
                self.management_cycles,

            "management_history_size":
                len(self.management_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_manager(self):

        try:

            result = (
                self.controller.recover_controller()
            )


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



    def stop_manager(self):

        result = (
            self.controller.stop_controller()
        )


        self.manager_status = RuntimeStatus.STOPPED


        return {

            "manager_status":
                self.manager_status.value,

            "controller":
                result,

            "stopped_at":
                self._time()
        }
