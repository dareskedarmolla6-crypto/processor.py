from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import RuntimeStatus


class IntelligenceRuntimeV11_87AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthMonitor:

    def __init__(self, health_runtime):

        self.health_runtime = health_runtime

        self.monitor_status = RuntimeStatus.INITIALIZED

        self.monitor_cycles = 0

        self.health_history = deque(
            maxlen=1000
        )

        self.alert_history = deque(
            maxlen=1000
        )



    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()



    def monitor_health(self):

        self.monitor_cycles += 1


        try:

            health_report = (
                self.health_runtime.health()
            )


            health_status = (
                health_report.get(
                    "health_status"
                )
            )


            if health_status == RuntimeStatus.ACTIVE.value:

                self.monitor_status = RuntimeStatus.ACTIVE


                alert = "NONE"


            else:

                self.monitor_status = RuntimeStatus.ERROR

                alert = "HEALTH_DEGRADED"



            record = {

                "cycle":
                    self.monitor_cycles,

                "health_status":
                    health_status,

                "monitor_status":
                    self.monitor_status.value,

                "alert":
                    alert,

                "checked_at":
                    self._time(),
            }


            self.health_history.append(
                record
            )


            if alert != "NONE":

                self.alert_history.append(
                    record
                )


            return {

                "monitor_status":
                    self.monitor_status.value,

                "health_status":
                    health_status,

                "alert":
                    alert,

                "monitor_cycles":
                    self.monitor_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.monitor_status = RuntimeStatus.ERROR


            record = {

                "cycle":
                    self.monitor_cycles,

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }


            self.alert_history.append(
                record
            )


            return {

                "monitor_status":
                    RuntimeStatus.ERROR.value,

                "alert":
                    "MONITOR_FAILURE",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def health(self):

        return {

            "autonomous_runtime_decision_governance_manager_runtime_health_monitor_available":
                True,

            "monitor_status":
                self.monitor_status.value,

            "monitor_cycles":
                self.monitor_cycles,

            "health_history_size":
                len(self.health_history),

            "alert_history_size":
                len(self.alert_history),

            "checked_at":
                self._time(),
        }



    def recover(self):

        self.monitor_status = RuntimeStatus.ACTIVE


        return {

            "recovery_status":
                "SUCCESS",

            "monitor_status":
                self.monitor_status.value,

            "checked_at":
                self._time(),
        }
