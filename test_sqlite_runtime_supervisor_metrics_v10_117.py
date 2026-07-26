import os
import tempfile

from market.sqlite_runtime_supervisor_metrics_repository import (
    SQLiteRuntimeSupervisorMetricsRepository
)


def test_sqlite_metrics_save_and_load():

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


        repository.save_metrics(
            {
                "starts": 5,
                "stops": 2,
                "restarts": 1,
                "recoveries": 3,
                "recovery_failures": 0
            }
        )


        metrics = (
            repository.load_metrics()
        )


        assert metrics == {
            "starts": 5,
            "stops": 2,
            "restarts": 1,
            "recoveries": 3,
            "recovery_failures": 0
        }


    finally:

        os.remove(
            db_path
        )



def test_sqlite_metrics_survive_restart():

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


        repository.save_metrics(
            {
                "starts": 10,
                "stops": 4,
                "restarts": 2,
                "recoveries": 6,
                "recovery_failures": 1
            }
        )


        # simulate application restart
        repository = (
            SQLiteRuntimeSupervisorMetricsRepository(
                db_path
            )
        )


        metrics = (
            repository.load_metrics()
        )


        assert metrics["starts"] == 10
        assert metrics["recoveries"] == 6
        assert metrics["recovery_failures"] == 1


    finally:

        os.remove(
            db_path
        )
