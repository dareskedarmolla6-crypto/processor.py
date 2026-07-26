from abc import ABC, abstractmethod


class RuntimeHealthRepository(ABC):
    """
    Production contract for runtime health persistence.

    Responsibilities:
        - Store runtime health snapshot
        - Restore runtime health snapshot

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Database implementation
    """

    @abstractmethod
    def save_health(
        self,
        health: dict
    ) -> None:
        """
        Persist runtime health snapshot.
        """
        raise NotImplementedError


    @abstractmethod
    def load_health(
        self
    ) -> dict:
        """
        Restore runtime health snapshot.
        """
        raise NotImplementedError
