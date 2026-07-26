class AutonomousExecutionSupervisorV10_145:
    """
    Supervisor with centralized state storage.
    """

    def __init__(
        self,
        health_monitor,
        recovery_manager,
        event_logger,
        metrics,
        state_store
    ):

        self.health_monitor = health_monitor
        self.recovery_manager = recovery_manager
        self.event_logger = event_logger
        self.metrics = metrics
        self.state_store = state_store


    def monitor(self):

        health = self.health_monitor.health()

        self.state_store.update_health(
            health
        )

        self.event_logger.record(
            "HEALTH_CHECK",
            health
        )

        # [ማስተካከያ] የ Signature Mismatch ችግርን ለመፍታት ወደ ሂስቶሪ ሌንግዝ ተቀይሯል ✅
        self.state_store.update_event_count(
            len(self.event_logger.history())
        )

        return health


    def recover_if_needed(self):

        health = self.monitor()

        if health["status"] != "UNHEALTHY":

            self.event_logger.record(
                "RECOVERY_SKIPPED",
                health
            )

            # [ማስተካከያ] የ Signature Mismatch ችግርን ለመፍታት ወደ ሂስቶሪ ሌንግዝ ተቀይሯል ✅
            self.state_store.update_event_count(
                len(self.event_logger.history())
            )

            return {
                "status": "NO_RECOVERY_REQUIRED"
            }

        result = self.recovery_manager.recover()

        self.metrics.record_recovery()

        self.state_store.increment_recovery()

        self.event_logger.record(
            "RECOVERY_COMPLETED",
            result
        )

        self.state_store.update_metrics(
            self.metrics.snapshot()
        )

        # [ማስተካከያ] የ Signature Mismatch ችግርን ለመፍታት ወደ ሂስቶሪ ሌንግዝ ተቀይሯል ✅
        self.state_store.update_event_count(
            len(self.event_logger.history())
        )

        return result


    def record_execution_result(
        self,
        success: bool
    ):

        self.metrics.record_execution(
            success
        )

        self.state_store.increment_execution()

        self.state_store.update_metrics(
            self.metrics.snapshot()
        )

        self.event_logger.record(
            "EXECUTION_RESULT",
            {
                "success": success
            }
        )

        # [ማስተካከያ] የ Signature Mismatch ችግርን ለመፍታት ወደ ሂስቶሪ ሌንግዝ ተቀይሯል ✅
        self.state_store.update_event_count(
            len(self.event_logger.history())
        )


    def status(self):

        return self.state_store.snapshot()
