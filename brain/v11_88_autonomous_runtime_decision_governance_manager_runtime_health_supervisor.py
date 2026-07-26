from datetime import datetime, timezone
from collections import deque

from brain.common.runtime_status import RuntimeStatus


class IntelligenceRuntimeV11_88AutonomousRuntimeDecisionGovernanceManagerRuntimeHealthSupervisor:

    def __init__(self, health_monitor):

        self.health_monitor = health_monitor

        self.supervisor_status = RuntimeStatus.INITIALIZED

        self.supervision_cycles = 0

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



    def supervise_health(self):

        self.supervision_cycles += 1


        try:

            monitor_report = (
                self.health_monitor.monitor_health()
            )


            monitor_status = (
                monitor_report.get(
                    "monitor_status"
                )
            )


            alert = (
                monitor_report.get(
                    "alert"
                )
            )


            if (
                monitor_status
                == RuntimeStatus.ACTIVE.value
                and alert == "NONE"
            ):

                self.supervisor_status = RuntimeStatus.ACTIVE

                decision = "ALLOW"


            else:

                self.supervisor_status = RuntimeStatus.ERROR

                decision = "BLOCK"



            record = {

                "cycle":
                    self.supervision_cycles,

                "monitor_status":
                    monitor_status,

                "decision":
                    decision,

                "alert":
                    alert,

                "checked_at":
                    self._time(),
            }


            self.supervision_history.append(
                record
            )


            return {

                "supervisor_status":
                    self.supervisor_status.value,

                "decision":
                    decision,

                "monitor":
                    monitor_report,

                "supervision_cycles":
                    self.supervision_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.supervisor_status = RuntimeStatus.ERROR


            return {

                "supervisor_status":
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

            "autonomous_runtime_decision_governance_manager_runtime_health_supervisor_available":
                True,

            "supervisor_status":
                self.supervisor_status.value,

            "supervision_cycles":
                self.supervision_cycles,

            "supervision_history_size":
                len(self.supervision_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "checked_at":
                self._time(),
        }



    def recover(self):

        try:

            recovery = (
                self.health_monitor.recover()
            )


            if (
                recovery.get("recovery_status")
                == "SUCCESS"
            ):

                self.supervisor_status = RuntimeStatus.ACTIVE

            else:

                self.supervisor_status = RuntimeStatus.ERROR



            event = {

                "event":
                    "RECOVERY_ATTEMPT",

                "status":
                    self.supervisor_status.value,

                "checked_at":
                    self._time(),
            }


            self.lifecycle_events.append(
                event
            )


            return {

                "recovery_status":
                    recovery.get(
                        "recovery_status"
                    ),

                "supervisor_status":
                    self.supervisor_status.value,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.supervisor_status = RuntimeStatus.ERROR


            return {

                "recovery_status":
                    "FAILED",

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }
