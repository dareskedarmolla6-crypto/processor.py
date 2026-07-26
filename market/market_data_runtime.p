from typing import List


class MarketDataRuntime:
    """
    Production market data runtime controller.

    Responsibilities:
        - Execute market data update cycles
        - Coordinate scheduler execution
        - Control runtime flow
        - Maintain runtime execution state snapshot
        - Expose runtime health metrics

    Does NOT contain:
        - Exchange communication
        - Market data generation
        - Symbol discovery
        - Trading decisions
    """

    def __init__(
        self,
        scheduler,
        logger=None
    ):
        self._scheduler = scheduler
        self._running = False

        # Dependency Injection ለፕሮዳክሽን ኦብስረቫቢሊቲ (Observability)
        self._logger = logger

        # የ Runtime ሁኔታ መከታተያ መዋቅር (State Snapshot Initializer)
        self._state = {
            "status": "STOPPED",
            "cycles": 0,
            "last_error": None
        }

    def run_cycle(
        self,
        symbols: List[str]
    ) -> None:
        """
        Execute one runtime cycle.
        """

        if not symbols:
            raise ValueError(
                "Symbols cannot be empty"
            )

        self._scheduler.run_once(
            symbols
        )

    def run_loop(
        self,
        symbols: List[str],
        cycles: int
    ) -> None:
        """
        Controlled runtime execution loop.

        Production scheduler controls timing.
        This method coordinates cycles and maintains internal metrics.
        """

        if not self._running:
            raise RuntimeError(
                "Runtime is not running"
            )

        if cycles <= 0:
            raise ValueError(
                "Cycles must be positive"
            )

        for _ in range(cycles):

            if self._logger:
                self._logger(
                    "runtime_cycle_started"
                )

            try:
                self.run_cycle(
                    symbols
                )

                # የስኬት ፍሰት ግዛት ማሻሻያ (Success State Tracking)
                self._state["cycles"] += 1
                self._state["status"] = "RUNNING"
                self._state["last_error"] = None

                if self._logger:
                    self._logger(
                        "runtime_cycle_completed"
                    )

            except Exception as e:

                # # የስህተት ፍሰት ግዛት ማሻሻያ (Error State Tracking)
                self._state["status"] = "ERROR"
                self._state["last_error"] = str(e)

                if self._logger:
                    self._logger(
                        f"runtime_error:{e}"
                    )

                raise

    def start(
        self
    ) -> None:
        """
        Mark runtime as active.
        """

        self._running = True
        # የመነሻ ሁኔታ ማሻሻያ
        self._state["status"] = "RUNNING"

    def stop(
        self
    ) -> None:
        """
        Gracefully stop runtime.
        """

        self._running = False
        # የማቆሚያ ሁኔታ ማሻሻያ
        self._state["status"] = "STOPPED"

    def restart(
        self
    ) -> None:
        """
        Restart runtime after stop or error.

        Preserves execution metrics.
        Does not reset cycle history.
        """

        self._running = True

        self._state["status"] = "RUNNING"
        self._state["last_error"] = None

    @property
    def running(
        self
    ) -> bool:
        return self._running

    def state(self) -> dict:
        """
        Return runtime execution state snapshot.
        """

        return self._state.copy()

    def health(self) -> dict:
        """
        Return runtime health status snapshot.

        Health depends on current runtime state.
        """

        status = self._state["status"]

        return {
            "status": status,
            "healthy": status == "RUNNING",
            "cycles": self._state["cycles"],
            "last_error": self._state["last_error"]
        }
