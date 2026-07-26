from market.in_memory_runtime_health_repository import (
    InMemoryRuntimeHealthRepository
)


def test_save_and_load_health():

    repo = InMemoryRuntimeHealthRepository()

    health = {
        "status": "RUNNING",
        "healthy": True,
        "cycles": 10
    }

    repo.save_health(
        health
    )

    loaded = repo.load_health()

    assert loaded == health



def test_health_snapshot_is_copy():

    repo = InMemoryRuntimeHealthRepository()

    health = {
        "status": "RUNNING"
    }

    repo.save_health(
        health
    )

    loaded = repo.load_health()

    loaded["status"] = "ERROR"

    assert repo.load_health()["status"] == "RUNNING"
