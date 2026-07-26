from market.sqlite_runtime_health_repository import (
    SQLiteRuntimeHealthRepository
)


def test_sqlite_save_and_load_health(
    tmp_path
):

    db = tmp_path / "health.db"

    repo = SQLiteRuntimeHealthRepository(
        str(db)
    )

    health = {
        "status": "RUNNING",
        "healthy": True,
        "cycles": 25,
        "last_error": None
    }

    repo.save_health(
        health
    )

    loaded = repo.load_health()

    assert loaded == health



def test_sqlite_updates_existing_health(
    tmp_path
):

    db = tmp_path / "health.db"

    repo = SQLiteRuntimeHealthRepository(
        str(db)
    )

    first = {
        "status": "RUNNING",
        "healthy": True,
        "cycles": 10,
        "last_error": None
    }

    second = {
        "status": "ERROR",
        "healthy": False,
        "cycles": 10,
        "last_error": "failure"
    }

    repo.save_health(
        first
    )

    repo.save_health(
        second
    )

    loaded = repo.load_health()

    assert loaded == second



def test_sqlite_empty_health(
    tmp_path
):

    db = tmp_path / "health.db"

    repo = SQLiteRuntimeHealthRepository(
        str(db)
    )

    loaded = repo.load_health()

    assert loaded == {}
