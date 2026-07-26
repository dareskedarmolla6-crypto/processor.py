import sqlite3

from market.sqlite_runtime_supervisor_metrics_repository import (
    SQLiteRuntimeSupervisorMetricsRepository
)


def test_sqlite_save_and_load_metrics(tmp_path):

    db_path = tmp_path / "supervisor_metrics.db"

    repository = (
        SQLiteRuntimeSupervisorMetricsRepository(
            str(db_path)
        )
    )

    metrics = {
        "recoveries": 5,
        "recovery_failures": 2
    }

    repository.save_metrics(
        metrics
    )

    loaded = (
        repository.load_metrics()
    )

    assert loaded == metrics



def test_sqlite_updates_existing_metrics(tmp_path):

    db_path = tmp_path / "supervisor_metrics.db"

    repository = (
        SQLiteRuntimeSupervisorMetricsRepository(
            str(db_path)
        )
    )

    repository.save_metrics(
        {
            "recoveries": 1,
            "recovery_failures": 0
        }
    )

    repository.save_metrics(
        {
            "recoveries": 3,
            "recovery_failures": 1
        }
    )

    loaded = (
        repository.load_metrics()
    )

    assert loaded["recoveries"] == 3
    assert loaded["recovery_failures"] == 1



def test_sqlite_empty_metrics(tmp_path):

    db_path = tmp_path / "supervisor_metrics.db"

    repository = (
        SQLiteRuntimeSupervisorMetricsRepository(
            str(db_path)
        )
    )

    loaded = (
        repository.load_metrics()
    )

    assert loaded == {}
