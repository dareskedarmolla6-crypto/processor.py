import os
import tempfile

from market.market_data_runtime_supervisor import (
    MarketDataRuntimeSupervisor
)

from market.sqlite_runtime_supervisor_metrics_repository import (
    SQLiteRuntimeSupervisorMetricsRepository
)


class RuntimeStub:

    def __init__(self):
        self._running = False
        self.restart_called = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    def restart(self):
        self.restart_called = True
        self._running = True
        return {
            "status": "RUNNING"
        }

    def health(self):
        return {
            "status": "RUNNING",
            "healthy": True
        }

    @property
    def running(self):
        return self._running


def test_supervisor_metrics_persist_to_sqlite():

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as file:
        db_path = file.name

    try:
        repository = (
            SQLiteRuntimeSupervisorMetricsRepository(
                db_path
            )
        )

        runtime = RuntimeStub()

        supervisor = (
            MarketDataRuntimeSupervisor(
                runtime,
                metrics_repository=repository
            )
        )

        supervisor.start()

        metrics = (
            repository.load_metrics()
        )

        assert metrics["starts"] == 1

    finally:
        os.remove(
            db_path
        )


def test_supervisor_restore_metrics_after_restart():

    with tempfile.NamedTemporaryFile(
        delete=False
    ) as file:
        db_path = file.name

    try:
        repository = (
            SQLiteRuntimeSupervisorMetricsRepository(
                db_path
            )
        )

        runtime = RuntimeStub()

        supervisor = (
            MarketDataRuntimeSupervisor(
                runtime,
                metrics_repository=repository
            )
        )

        supervisor.start()

        # simulate application restart
        repository = (
            SQLiteRuntimeSupervisorMetricsRepository(
                db_path
            )
        )

        supervisor2 = (
            MarketDataRuntimeSupervisor(
                runtime,
                metrics_repository=repository
            )
        )

        metrics = (
            supervisor2.metrics()
        )

        assert metrics["starts"] == 1

    finally:
        os.remove(
            db_path
        )
