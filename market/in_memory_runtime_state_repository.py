from market.runtime_state_repository import (
    RuntimeStateRepository
)


class InMemoryRuntimeStateRepository(
    RuntimeStateRepository
):
    """
    In-memory implementation of runtime state repository.

    Used for:
        - Contract verification
        - Dependency testing

    Not used as production persistence.
    """

    def __init__(self):

        self._state = None

    def save_state(
        self,
        state: dict
    ) -> None:

        self._state = state.copy()

    def load_state(
        self
    ) -> dict:

        if self._state is None:
            return {}

        return self._state.copy()
