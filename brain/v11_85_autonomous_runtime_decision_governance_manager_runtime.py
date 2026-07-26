from datetime import datetime, timezone

from brain.common.runtime_status import (
    RuntimeStatus,
    DecisionStatus,
)


class IntelligenceRuntimeV11_85AutonomousRuntimeDecisionGovernanceManagerRuntime:

    VALID_DECISIONS = {
        DecisionStatus.ALLOW,
        DecisionStatus.BLOCK,
    }

    def __init__(self, coordinator_runtime):

        self.coordinator_runtime = coordinator_runtime

        self.manager_status = RuntimeStatus.INITIALIZED
        self.last_decision = None

        self.management_cycles = 0
        self.decision_history = []


    def _time(self):

        return datetime.now(timezone.utc).isoformat()


    def manage_runtime_governance(self):

        self.management_cycles += 1

        record = {
            "cycle": self.management_cycles,
            "started_at": self._time(),
        }

        try:

            coordination = (
                self.coordinator_runtime
                .coordinate_runtime_governance()
            )


            decision_raw = coordination.get(
                "decision"
            )


            decision = DecisionStatus.BLOCK

            for valid_dec in self.VALID_DECISIONS:

                if (
                    valid_dec.value == decision_raw
                    or valid_dec == decision_raw
                ):
                    decision = valid_dec
                    break


            self.last_decision = decision


            if (
                coordination.get("coordination_status")
                == RuntimeStatus.ACTIVE.value
                and decision == DecisionStatus.ALLOW
            ):

                self.manager_status = RuntimeStatus.ACTIVE

            else:

                self.manager_status = RuntimeStatus.ERROR



            record["decision"] = decision.value
            record["status"] = "SUCCESS"
            record["completed_at"] = self._time()

            self.decision_history.append(record)


            return {

                "management_status":
                    self.manager_status.value,

                "runtime_status":
                    "ACTIVE"
                    if self.manager_status == RuntimeStatus.ACTIVE
                    else "ERROR",

                "decision":
                    decision.value,

                "coordination":
                    coordination,

                "management_cycles":
                    self.management_cycles,

                "checked_at":
                    self._time(),
            }



        except Exception as error:


            self.manager_status = RuntimeStatus.ERROR
            self.last_decision = DecisionStatus.BLOCK


            record["status"] = "FAILED"
            record["error"] = str(error)

            self.decision_history.append(record)


            return {

                "management_status":
                    "FAILED",

                "runtime_status":
                    "ERROR",

                "decision":
                    DecisionStatus.BLOCK.value,

                "error":
                    str(error),

                "checked_at":
                    self._time(),
            }



    def health(self):

        return {

            "autonomous_runtime_decision_governance_manager_runtime_available":
                True,

            "manager_status":
                self.manager_status.value,

            "runtime_status":
                "ACTIVE"
                if self.manager_status == RuntimeStatus.ACTIVE
                else "ERROR",

            "last_decision":
                self.last_decision.value
                if self.last_decision
                else None,

            "management_cycles":
                self.management_cycles,

            "decision_history_size":
                len(self.decision_history),

            "checked_at":
                self._time(),
        }
