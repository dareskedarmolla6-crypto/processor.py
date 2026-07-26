
from datetime import datetime, timezone


class AutonomousRuntimeGovernanceFoundationV12:

    VALID_STATUS = {
        "INITIALIZED",
        "ACTIVE",
        "ERROR",
        "STOPPED",
        "RECOVERY",
    }

    VALID_DECISIONS = {
        "ALLOW",
        "BLOCK",
    }


    def __init__(
        self,
        runtime_supervisor,
        execution_controller,
        orchestrator,
        full_system,
    ):

        self.runtime_supervisor = runtime_supervisor
        self.execution_controller = execution_controller
        self.orchestrator = orchestrator
        self.full_system = full_system

        self.runtime_status = "INITIALIZED"

        self.cycles = 0
        self.last_decision = None
        self.last_error = None

        self.started_at = None
        self.last_cycle_at = None

        self.lifecycle_events = []
        self.audit_history = []


    def _time(self):

        return datetime.now(
            timezone.utc
        ).isoformat()


    def _event(self, name, data=None):

        self.lifecycle_events.append(
            {
                "event": name,
                "data": data,
                "timestamp": self._time(),
            }
        )


    def validate_dependencies(self):

        dependencies = {

            "runtime_supervisor":
                self.runtime_supervisor is not None,

            "execution_controller":
                self.execution_controller is not None,

            "orchestrator":
                self.orchestrator is not None,

            "full_system":
                self.full_system is not None,
        }


        return {

            "ready":
                all(dependencies.values()),

            "dependencies":
                dependencies,

            "checked_at":
                self._time(),
        }


    def start_runtime(self):

        check = self.validate_dependencies()


        if not check["ready"]:

            self.runtime_status = "ERROR"

            return {
                "runtime_status": "ERROR",
                "dependency": check,
            }


        self.runtime_status = "ACTIVE"
        self.started_at = self._time()


        self._event(
            "RUNTIME_STARTED"
        )


        return {

            "runtime_status":
                "ACTIVE",

            "started_at":
                self.started_at,
        }


    def execute_cycle(
        self,
        balance,
        symbol=None,
        stop_loss_price=None,
    ):

        if self.runtime_status != "ACTIVE":

            start = self.start_runtime()

            if start["runtime_status"] != "ACTIVE":

                return start


        if symbol is None:

            symbol = (
                self.full_system
                .market_manager
                .select_best_symbol()
            )

            if symbol is None:

                return {
                    "runtime_status": "ERROR",
                    "decision": "BLOCK",
                    "error": "NO_ACTIVE_SYMBOL_AVAILABLE",
                }


        self.cycles += 1


        try:

            governance = (
                self.orchestrator
                .orchestrate_execution()
            )


            decision = governance.get(
                "decision",
                "BLOCK",
            )


            if decision not in self.VALID_DECISIONS:

                decision = "BLOCK"


            self.last_decision = decision


            if decision == "ALLOW":

                execution = (
                    self.full_system.run(
                        symbol,
                        balance,
                        stop_loss_price,
                    )
                )

            else:

                execution = {
                    "status": "BLOCKED"
                }


            self.last_cycle_at = self._time()


            self.audit_history.append(
                {
                    "cycle": self.cycles,
                    "decision": decision,
                    "execution": execution,
                    "timestamp": self.last_cycle_at,
                }
            )


            return {

                "runtime_status":
                    self.runtime_status,

                "cycle":
                    self.cycles,

                "decision":
                    decision,

                "governance":
                    governance,

                "execution":
                    execution,

                "timestamp":
                    self.last_cycle_at,
            }


        except Exception as error:

            self.runtime_status = "ERROR"
            self.last_error = str(error)


            return {

                "runtime_status":
                    "ERROR",

                "decision":
                    "BLOCK",

                "error":
                    str(error),
            }


    def recover_runtime(self):

        self.runtime_status = "RECOVERY"


        if hasattr(
            self.runtime_supervisor,
            "recover_runtime"
        ):

            result = (
                self.runtime_supervisor
                .recover_runtime()
            )


            if result.get(
                "recovery_status"
            ) == "SUCCESS":

                self.runtime_status = "ACTIVE"

                return result


        self.runtime_status = "ERROR"


        return {

            "recovery_status":
                "FAILED",

            "runtime_status":
                "ERROR",
        }


    def health(self):

        return {

            "v12_foundation_available":
                True,

            "v12_runtime_available":
                True,

            "runtime_status":
                self.runtime_status,

            "cycles":
                self.cycles,

            "last_decision":
                self.last_decision,

            "audit_records":
                len(self.audit_history),

            "lifecycle_events":
                len(self.lifecycle_events),

            "last_error":
                self.last_error,

            "checked_at":
                self._time(),
        }
