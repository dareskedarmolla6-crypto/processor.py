from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import RuntimeStatus


class IntelligenceRuntimeV11_86AutonomousRuntimeDecisionGovernanceManagerRuntimeHealth:

    def __init__(self, manager_runtime):

        self.manager_runtime = manager_runtime

        self.health_checks = deque(
            maxlen=1000
        )

        self.lifecycle_events = deque(
            maxlen=1000
        )

        self.health_status = RuntimeStatus.INITIALIZED



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def validate_dependency(self):

        try:

            available = (
                self.manager_runtime
                is not None
            )


            if available:

                status = RuntimeStatus.ACTIVE

            else:

                status = RuntimeStatus.ERROR


            result = {

                "dependency_available":
                    available,

                "dependency_status":
                    status.value,

                "checked_at":
                    self._time(),
            }


            return result


        except Exception as error:


            return {

                "dependency_available":
                    False,

                "dependency_status":
                    RuntimeStatus.ERROR.value,

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def health(self):

        dependency = (
            self.validate_dependency()
        )


        try:

            manager_health = (
                self.manager_runtime.health()
            )


            if (
                dependency["dependency_available"]
                and manager_health.get("runtime_status")
                == RuntimeStatus.ACTIVE.value
            ):

                self.health_status = RuntimeStatus.ACTIVE

            else:

                self.health_status = RuntimeStatus.ERROR



            report = {

                "autonomous_runtime_decision_governance_manager_runtime_health_available":
                    True,

                "health_status":
                    self.health_status.value,

                "dependency":
                    dependency,

                "manager_health":
                    manager_health,

                "health_checks":
                    len(self.health_checks) + 1,

                "checked_at":
                    self._time(),
            }


            self.health_checks.append(
                report
            )


            return report



        except Exception as error:


            self.health_status = RuntimeStatus.ERROR


            report = {

                "autonomous_runtime_decision_governance_manager_runtime_health_available":
                    False,

                "health_status":
                    RuntimeStatus.ERROR.value,

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }


            self.health_checks.append(
                report
            )


            return report



    def recover(self):

        try:

            if self.manager_runtime is None:

                self.health_status = RuntimeStatus.ERROR

                return {

                    "recovery_status":
                        "FAILED",

                    "reason":
                        "MANAGER_RUNTIME_UNAVAILABLE",

                    "checked_at":
                        self._time(),
                }



            self.health_status = RuntimeStatus.ACTIVE


            event = {

                "event":
                    "RECOVERY_SUCCESS",

                "checked_at":
                    self._time(),
            }


            self.lifecycle_events.append(
                event
            )


            return {

                "recovery_status":
                    "SUCCESS",

                "health_status":
                    self.health_status.value,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.health_status = RuntimeStatus.ERROR


            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }
