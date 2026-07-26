from datetime import datetime, timezone


class IntelligenceRuntimeV11_71RuntimeGovernanceEngine:


    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(self, governance_manager):

        self.governance_manager = governance_manager

        self.runtime_status = "INITIALIZED"

        self.last_decision = None

        self.governance_cycles = 0

        self.decision_history = []



    def _time(self):

        return datetime.now(timezone.utc).isoformat()



    def evaluate_runtime(self):

        self.governance_cycles += 1


        record = {

            "cycle": self.governance_cycles,

            "started_at": self._time(),

        }


        try:

            result = (
                self.governance_manager.manage_governance()
            )


            if (
                result.get("management_status")
                != "ACTIVE"
            ):

                self.runtime_status = "BLOCKED"

                self.last_decision = "BLOCK"


                record["decision"] = "BLOCK"

                record["status"] = "FAILED"

                self.decision_history.append(
                    record
                )


                return {

                    "runtime_status":
                        "BLOCKED",

                    "decision":
                        "BLOCK",

                    "governance":
                        result,

                    "checked_at":
                        self._time(),

                }



            decision = (
                result.get(
                    "decision"
                )
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"



            self.last_decision = decision


            if decision == "ALLOW":

                self.runtime_status = "ACTIVE"

            else:

                self.runtime_status = "BLOCKED"



            record["decision"] = decision

            record["status"] = "SUCCESS"

            record["completed_at"] = self._time()


            self.decision_history.append(
                record
            )


            return {

                "runtime_status":
                    self.runtime_status,

                "decision":
                    decision,

                "governance":
                    result,

                "governance_cycles":
                    self.governance_cycles,

                "checked_at":
                    self._time(),

            }



        except Exception as error:


            self.runtime_status = "ERROR"

            self.last_decision = "BLOCK"


            return {

                "runtime_status":
                    "ERROR",

                "decision":
                    "BLOCK",

                "error":
                    str(error),

                "checked_at":
                    self._time(),

            }



    def health(self):

        try:

            dependency_health = (
                self.governance_manager.health()
            )


        except Exception as error:

            dependency_health = {

                "runtime_status":
                    "FAILED",

                "error":
                    str(error),

            }


            return {

                "runtime_governance_available":
                    True,

                "runtime_status":
                    "ERROR",

                "last_decision":
                    self.last_decision,

                "dependency_health":
                    dependency_health,

                "checked_at":
                    self._time(),

            }



        return {

            "runtime_governance_available":
                True,

            "runtime_status":
                self.runtime_status,

            "last_decision":
                self.last_decision,

            "governance_cycles":
                self.governance_cycles,

            "decision_history_size":
                len(self.decision_history),

            "dependency_health":
                dependency_health,

            "checked_at":
                self._time(),

        }
