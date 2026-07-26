from brain.execution_supervisor_persistence import (
    ExecutionSupervisorPersistence
)


class StubPersistence:

    def __init__(self):

        self.saved = []
        self.closed = []


    def save_position(
        self,
        position
    ):

        self.saved.append(position)


    def close_position(
        self,
        position
    ):

        self.closed.append(position)


    def restore_positions(self):

        return self.saved



def test_save_open_position():

    persistence = StubPersistence()

    bridge = ExecutionSupervisorPersistence(
        persistence
    )


    position = {
        "id": 1,
        "symbol": "BTCUSDT"
    }


    result = bridge.save_open_position(
        position
    )


    assert result["status"] == "SAVED"

    assert len(
        persistence.saved
    ) == 1



def test_restore_positions():

    persistence = StubPersistence()

    persistence.saved.append(
        {
            "id": 2,
            "symbol": "ETHUSDT"
        }
    )


    bridge = ExecutionSupervisorPersistence(
        persistence
    )


    result = bridge.restore()


    assert len(result) == 1

    assert result[0]["symbol"] == "ETHUSDT"



def test_save_closed_position():

    persistence = StubPersistence()

    bridge = ExecutionSupervisorPersistence(
        persistence
    )


    position = {
        "id": 3,
        "symbol": "SOLUSDT"
    }


    result = bridge.save_closed_position(
        position
    )


    assert result["status"] == "UPDATED"

    assert len(
        persistence.closed
    ) == 1
