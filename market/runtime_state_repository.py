from abc import ABC, abstractmethod


class RuntimeStateRepository(ABC):
    """
    Production contract for runtime state persistence.

    Responsibilities:
        - Save runtime state
        - Load runtime state

    Does NOT contain:
        - Runtime execution logic
        - Scheduler logic
        - Market data logic
    """

    @abstractmethod
    def save_state(
        self,
        state: dict
    ) -> None:
        """
        Persist runtime state.
        """
        pass

    @abstractmethod
    def load_state(
        self
    ) -> dict:
        """
        Load persisted runtime state.
        """
        pass
