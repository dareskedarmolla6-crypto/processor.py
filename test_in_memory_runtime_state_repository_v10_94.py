from market.in_memory_runtime_state_repository import (
    InMemoryRuntimeStateRepository
)


def test_save_and_load_state():

    repo = InMemoryRuntimeStateRepository()

    state = {
        "status": "RUNNING",
        "cycles": 10,
        "last_error": None
    }

    repo.save_state(
        state
    )

    loaded = repo.load_state()

    assert loaded == state


def test_state_snapshot_is_copy():

    repo = InMemoryRuntimeStateRepository()

    state = {
        "status": "RUNNING"
    }

    repo.save_state(
        state
    )

    loaded = repo.load_state()

    loaded["status"] = "ERROR"

    assert repo.load_state()["status"] == "RUNNING"
