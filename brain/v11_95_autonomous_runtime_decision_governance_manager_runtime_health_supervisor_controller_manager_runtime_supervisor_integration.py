from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_95AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisorControllerManagerRuntimeSupervisorIntegration:


    def __init__(self, manager):

        self.manager = manager

        self.integration_status = RuntimeStatus.INITIALIZED

        self.integration_cycles = 0

        self.last_decision = None

        self.integration_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start_integration(self):

        try:

            result = (
                self.manager.start_manager()
            )

            self.integration_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "INTEGRATION_START",
                    "time": self._time()
                }
            )


            return {

                "integration_status":
                    self.integration_status.value,

                "manager":
                    result,

                "started_at":
                    self._time()
            }



        except Exception as error:

            self.integration_status = RuntimeStatus.ERROR

            return {

                "integration_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def execute_runtime_cycle(self):

        self.integration_cycles += 1


        try:

            management = (
                self.manager.manage_control_cycle()
            )


            decision = management.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.integration_history.append(
                {
                    "cycle":
                        self.integration_cycles,

                    "decision":
                        decision,

                    "time":
                        self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.integration_status = RuntimeStatus.ACTIVE

            else:

                self.integration_status = RuntimeStatus.ERROR



            return {

                "integration_status":
                    self.integration_status.value,

                "decision":
                    decision,

                "management":
                    management,

                "integration_cycles":
                    self.integration_cycles,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.integration_status = RuntimeStatus.ERROR

            return {

                "integration_status":
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

            "integration_status":
                self.integration_status.value,

            "last_decision":
                self.last_decision,

            "integration_cycles":
                self.integration_cycles,

            "integration_history_size":
                len(self.integration_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_integration(self):

        try:

            result = (
                self.manager.recover_manager()
            )


            self.integration_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "manager":
                    result,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.integration_status = RuntimeStatus.ERROR

            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop_integration(self):

        result = (
            self.manager.stop_manager()
        )


        self.integration_status = RuntimeStatus.STOPPED


        return {

            "integration_status":
                self.integration_status.value,

            "manager":
                result,

            "stopped_at":
                self._time()
        }
