from .runtime_supervisor_metrics import (
    RuntimeSupervisorMetrics
)


class MarketDataRuntimeSupervisor:
    """
    Production runtime supervisor.

    V10.116 unified supervisor.

    Responsibilities:
        - Runtime lifecycle control
        - Health monitoring
        - Recovery execution
        - Event persistence
        - Metrics tracking

    Does NOT contain:
        - Market data logic
        - Exchange communication
        - Trading decisions
        - Storage implementation
    """


    def __init__(
        self,
        runtime,
        health_repository=None,
        event_repository=None,
        metrics_repository=None,
        metrics=None
    ):

        self._runtime = runtime

        self._health_repository = (
            health_repository
        )

        self._event_repository = (
            event_repository
        )


        self._metrics = (
            metrics
            or RuntimeSupervisorMetrics(
                repository=metrics_repository
            )
        )

        # V10.116 compatibility:
        # Persist initial lifecycle state immediately.
        self._metrics.persist_lifecycle()


    # -------------------------
    # Compatibility API
    # -------------------------

    @property
    def running(self):

        return getattr(
            self._runtime,
            "running",
            False
        )


    def health(self):

        return self.check_health()


    def metrics(self):

        return self._metrics.snapshot()



    # -------------------------
    # Lifecycle
    # -------------------------

    def start(self):

        self._runtime.start()

        self._metrics.increment(
            "starts"
        )

        self.check_health()



    def stop(self):

        self._runtime.stop()

        self._metrics.increment(
            "stops"
        )

        self.check_health()



    def restart(self):

        result = (
            self._runtime.restart()
        )

        self._metrics.increment(
            "restarts"
        )

        self.check_health()

        return result



    # -------------------------
    # Health
    # -------------------------

    def check_health(self):

        health = (
            self._runtime.health()
        )


        if self._health_repository:

            self._health_repository.save_health(
                health
            )


        return health


    # -------------------------
    # Recovery & Events
    # -------------------------

    def _record_event(
        self,
        event: str
    ) -> None:

        if self._event_repository:

            self._event_repository.save_event(
                event
            )


    def recover(self) -> dict:

        self._record_event(
            "recovery_started"
        )

        health = self.check_health()

        if health["healthy"]:

            return {
                "recovered": False,
                "reason": "runtime_healthy"
            }


        try:

            result = (
                self._runtime.restart()
            )

            post_health = self.check_health()


            if post_health["healthy"]:

                self._metrics.increment(
                    "recoveries"
                )

                # V10.107 contract alignment: success -> completed
                self._record_event(
                    "recovery_completed"
                )

                return {
                    "recovered": True,
                    "result": result
                }

            else:

                self._metrics.increment(
                    "recovery_failures"
                )

                self._record_event(
                    "recovery_failed"
                )

                return {
                    "recovered": False,
                    "reason": "recovery_failed_health_check"
                }


        except Exception as e:

            self._metrics.increment(
                "recovery_failures"
            )

            # V10.107 contract alignment: error -> failed
            self._record_event(
                "recovery_failed"
            )

            raise e
