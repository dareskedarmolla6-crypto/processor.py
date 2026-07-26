from market.sqlite_runtime_state_repository import (
    SQLiteRuntimeStateRepository
)


def test_sqlite_save_and_load_state(tmp_path):

    db_file = tmp_path / "runtime.db"

    repo = SQLiteRuntimeStateRepository(
        str(db_file)
    )

    state = {
        "status": "RUNNING",
        "cycles": 25,
        "last_error": None
    }

    repo.save_state(
        state
    )

    loaded = repo.load_state()

    assert loaded == state



def test_sqlite_updates_existing_state(tmp_path):

    db_file = tmp_path / "runtime.db"

    repo = SQLiteRuntimeStateRepository(
        str(db_file)
    )

    repo.save_state(
        {
            "status": "RUNNING",
            "cycles": 10,
            "last_error": None
        }
    )

    repo.save_state(
        {
            "status": "ERROR",
            "cycles": 11,
            "last_error": "connection failed"
        }
    )

    loaded = repo.load_state()

    assert loaded["status"] == "ERROR"
    assert loaded["cycles"] == 11
    assert loaded["last_error"] == "connection failed"



def test_sqlite_empty_state(tmp_path):

    db_file = tmp_path / "runtime.db"

    repo = SQLiteRuntimeStateRepository(
        str(db_file)
    )

    loaded = repo.load_state()

    assert loaded == {}
