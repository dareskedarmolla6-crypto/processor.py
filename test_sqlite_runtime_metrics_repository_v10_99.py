from market.sqlite_runtime_metrics_repository import (
    SQLiteRuntimeMetricsRepository
)


def test_sqlite_save_and_load_metrics(
    tmp_path
):

    db = tmp_path / "runtime_metrics.db"

    repo = SQLiteRuntimeMetricsRepository(
        str(db)
    )

    metrics = {
        "successful_cycles": 20,
        "failed_cycles": 3
    }

    repo.save_metrics(
        metrics
    )

    restored = repo.load_metrics()

    assert restored == metrics


def test_sqlite_updates_existing_metrics(
    tmp_path
):

    db = tmp_path / "runtime_metrics.db"

    repo = SQLiteRuntimeMetricsRepository(
        str(db)
    )

    repo.save_metrics(
        {
            "successful_cycles": 5,
            "failed_cycles": 1
        }
    )

    repo.save_metrics(
        {
            "successful_cycles": 15,
            "failed_cycles": 4
        }
    )

    restored = repo.load_metrics()

    assert restored == {
        "successful_cycles": 15,
        "failed_cycles": 4
    }


def test_sqlite_empty_metrics(
    tmp_path
):

    db = tmp_path / "runtime_metrics.db"

    repo = SQLiteRuntimeMetricsRepository(
        str(db)
    )

    assert repo.load_metrics() == {}
