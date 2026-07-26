class AutonomousExecutionSupervisorV10_141:
    """
    Supervisor with execution event tracking.
    """


    def __init__(
        self,
        health_monitor,
        recovery_manager,
        event_logger
    ):

        self.health_monitor = health_monitor
        self.recovery_manager = recovery_manager
        self.event_logger = event_logger



    def check_health(self):

        health = self.health_monitor.health()

        self.event_logger.record(
            "HEALTH_CHECK",
            health
        )

        return health



    def recover_if_needed(self):

        health = self.check_health()


        if health["status"] == "UNHEALTHY":

            self.event_logger.record(
                "RECOVERY_STARTED",
                health
            )


            result = self.recovery_manager.recover()


            self.event_logger.record(
                "RECOVERY_COMPLETED",
                result
            )


            return result


        self.event_logger.record(
            "RECOVERY_SKIPPED",
            health
        )


        return {
            "status": "NO_RECOVERY_REQUIRED"
        }



    def status(self):

        return {
            "health": self.check_health(),
            "events": len(
                self.event_logger.history()
            )
        }
