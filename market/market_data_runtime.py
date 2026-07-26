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
        - Record runtime lifecycle event history
        - Track granular cycle metrics
        - Delegate state persistence and recovery to repository layer
        - Delegate event persistence and recovery to event repository layer
        - Delegate metrics persistence and recovery to metrics repository layer
        - Delegate health persistence and recovery to health repository layer
    """

    def __init__(
        self,
        scheduler,
        manager=None,
        logger=None,
        state_repository=None,
        event_repository=None,
        metrics_repository=None,
        health_repository=None
    ):
        self._scheduler = scheduler
        self._manager = manager
        self._running = False

        self._logger = logger
        self._state_repository = state_repository
        self._event_repository = event_repository
        self._metrics_repository = metrics_repository
        self._health_repository = health_repository

        self._state = {
            "status": "STOPPED",
            "cycles": 0,
            "last_error": None
        }

        self._events = []

        self._metrics = {
            "successful_cycles": 0,
            "failed_cycles": 0
        }

        # የደህንነት መልሶ ማግኛ ጥሪዎች
        self.restore_state()
        self.restore_events()
        self.restore_metrics()
        self.restore_health()

    def start(self) -> None:
        """Start the runtime execution lifecycle."""
        self._running = True
        self._state["status"] = "RUNNING"

        self._persist_state()
        self._persist_health()
        self._record_event("runtime_started")

    def stop(self) -> None:
        """Stop the runtime execution lifecycle."""
        self._running = False
        self._state["status"] = "STOPPED"

        self._persist_state()
        self._persist_health()
        self._record_event("runtime_stopped")

    def restart(self) -> None:
        """Restart runtime cleanly while preserving execution statistics."""
        self.stop()
        self.start()

    def run_cycle(self, symbols: List[str] = None) -> None:
        """
        Execute one market data cycle.
        """
        if symbols is None:
            if not self._manager:
                raise ValueError("Market manager unavailable")

            symbols = self._manager.active_symbols()

        if not symbols:
            raise ValueError("Symbols cannot be empty")

        self._scheduler.run_once(symbols)

    def run_loop(self, symbols: List[str], cycles: int) -> None:
        """Controlled runtime execution loop with unified telemetry update."""
        if not self._running:
            raise RuntimeError("Runtime is not running")

        if cycles <= 0:
            raise ValueError("Cycles must be positive")

        for _ in range(cycles):
            self._record_event("cycle_started")
            try:
                self.run_cycle(symbols)

                self._state["cycles"] += 1
                self._state["status"] = "RUNNING"
                self._state["last_error"] = None

                self._metrics["successful_cycles"] += 1

                self._persist_state()
                self._persist_metrics()
                self._persist_health()

                self._record_event("cycle_completed")

            except Exception as e:
                self._state["status"] = "ERROR"
                self._state["last_error"] = str(e)
                self._metrics["failed_cycles"] += 1

                self._persist_state()
                self._persist_metrics()
                self._persist_health()

                self._record_event("runtime_error")
                self._record_event("cycle_failed")
                raise e

    def _record_event(self, event: str) -> None:
        """Unified Event Chokepoint: Records to memory, persistence, and logger."""
        self._events.append(event)

        if self._event_repository:
            self._event_repository.save_event(event)

        if self._logger:
            self._logger(event)

    # ==========================================
    # PERSISTENCE HELPERS
    # ==========================================

    def _persist_state(self) -> None:
        if self._state_repository:
            self._state_repository.save_state(self._state)

    def _persist_metrics(self) -> None:
        if self._metrics_repository:
            self._metrics_repository.save_metrics(self._metrics)

    def _persist_health(self) -> None:
        if self._health_repository:
            self._health_repository.save_health(self.get_health())

    # ==========================================
    # RESTORATION HELPERS
    # ==========================================

    def restore_state(self) -> None:
        """
        Production safe-restart state restoration.
        Preserves metrics, but resets status to STOPPED to ensure clean boot.
        """
        if self._state_repository:
            saved = self._state_repository.load_state()
            if saved:
                self._state["cycles"] = saved.get("cycles", 0)
                self._state["last_error"] = saved.get("last_error")
                self._state["status"] = "STOPPED"  # Always start safely

    def restore_events(self) -> None:
        if self._event_repository:
            saved = self._event_repository.load_events()
            if saved is not None:
                self._events = saved

    def restore_metrics(self) -> None:
        if self._metrics_repository:
            saved = self._metrics_repository.load_metrics()
            if saved:
                self._metrics = saved

    def restore_health(self) -> None:
        """
        Granular health restoration including historical errors.
        """
        if self._health_repository:
            saved = self._health_repository.load_health()
            if saved:
                if "status" in saved:
                    self._state["status"] = saved["status"]
                if "cycles" in saved:
                    self._state["cycles"] = saved["cycles"]
                if "last_error" in saved:
                    self._state["last_error"] = saved["last_error"]

    # ==========================================
    # EXPOSE HEALTH METRICS
    # ==========================================

    def get_health(self) -> dict:
        """Expose runtime health metrics cleanly."""
        status = self._state["status"]
        return {
            "status": status,
            "healthy": status == "RUNNING",
            "cycles": self._state["cycles"],
            "last_error": self._state["last_error"]
        }

    # ==========================================
    # BACKWARD-COMPATIBLE API
    # ==========================================

    @property
    def running(self) -> bool:
        return self._running

    def state(self) -> dict:
        return self._state.copy()

    def events(self) -> list:
        return self._events.copy()

    def metrics(self) -> dict:
        return self._metrics.copy()

    def health(self) -> dict:
        return self.get_health()
