from .runtime_health_repository import RuntimeHealthRepository


class InMemoryRuntimeHealthRepository(
    RuntimeHealthRepository
):
    """
    In-memory implementation for runtime health persistence.

    Responsibilities:
        - Store runtime health snapshot
        - Restore runtime health snapshot

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Database implementation
    """

    def __init__(
        self
    ):
        self._health = None


    def save_health(
        self,
        health: dict
    ) -> None:
        """
        Save health snapshot.

        Stores copy to prevent
        external mutation.
        """

        self._health = health.copy()


    def load_health(
        self
    ) -> dict:
        """
        Restore health snapshot.

        Returns copy.
        """

        if self._health is None:
            return {}

        return self._health.copy()
