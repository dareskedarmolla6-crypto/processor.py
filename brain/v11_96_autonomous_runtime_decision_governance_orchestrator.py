from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_96AutonomousRuntimeDecisionGovernanceOrchestrator:


    def __init__(self, integration_runtime):

        self.integration_runtime = integration_runtime

        self.orchestrator_status = RuntimeStatus.INITIALIZED

        self.orchestration_cycles = 0

        self.last_decision = None

        self.orchestration_history = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )


    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def start_orchestrator(self):

        try:

            result = (
                self.integration_runtime
                .start_integration()
            )


            self.orchestrator_status = RuntimeStatus.ACTIVE


            self.lifecycle_events.append(
                {
                    "event": "ORCHESTRATOR_START",
                    "time": self._time()
                }
            )


            return {

                "orchestrator_status":
                    self.orchestrator_status.value,

                "integration":
                    result,

                "started_at":
                    self._time()
            }



        except Exception as error:

            self.orchestrator_status = RuntimeStatus.ERROR

            return {

                "orchestrator_status":
                    "ERROR",

                "error":
                    str(error)
            }



    def execute_orchestration_cycle(self):

        self.orchestration_cycles += 1


        try:

            runtime_result = (
                self.integration_runtime
                .execute_runtime_cycle()
            )


            decision = runtime_result.get(
                "decision",
                DecisionStatus.BLOCK.value
            )


            self.last_decision = decision


            self.orchestration_history.append(
                {
                    "cycle":
                        self.orchestration_cycles,

                    "decision":
                        decision,

                    "time":
                        self._time()
                }
            )


            if decision == DecisionStatus.ALLOW.value:

                self.orchestrator_status = RuntimeStatus.ACTIVE

            else:

                self.orchestrator_status = RuntimeStatus.ERROR



            return {

                "orchestrator_status":
                    self.orchestrator_status.value,

                "decision":
                    decision,

                "runtime":
                    runtime_result,

                "orchestration_cycles":
                    self.orchestration_cycles,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.orchestrator_status = RuntimeStatus.ERROR

            return {

                "orchestrator_status":
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

            "orchestrator_status":
                self.orchestrator_status.value,

            "last_decision":
                self.last_decision,

            "orchestration_cycles":
                self.orchestration_cycles,

            "history_size":
                len(self.orchestration_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time()
        }



    def recover_orchestrator(self):

        try:

            result = (
                self.integration_runtime
                .recover_integration()
            )


            self.orchestrator_status = RuntimeStatus.ACTIVE


            return {

                "recovery_status":
                    "SUCCESS",

                "integration":
                    result,

                "checked_at":
                    self._time()
            }



        except Exception as error:

            self.orchestrator_status = RuntimeStatus.ERROR

            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error)
            }



    def stop_orchestrator(self):

        result = (
            self.integration_runtime
            .stop_integration()
        )


        self.orchestrator_status = RuntimeStatus.STOPPED


        return {

            "orchestrator_status":
                self.orchestrator_status.value,

            "integration":
                result,

            "stopped_at":
                self._time()
        }
