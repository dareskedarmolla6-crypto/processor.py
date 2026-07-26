from abc import ABC, abstractmethod


class RuntimeEventRepository(ABC):
    """
    Production contract for runtime event persistence.

    Responsibilities:
        - Store runtime lifecycle events
        - Retrieve historical runtime events

    Does NOT contain:
        - Runtime control logic
        - Scheduler logic
        - Market data logic
        - Database implementation
    """

    @abstractmethod
    def save_event(
        self,
        event: str
    ) -> None:
        """
        Persist single runtime event.
        """
        raise NotImplementedError


    @abstractmethod
    def load_events(
        self
    ) -> list:
        """
        Load runtime event history.
        """
        raise NotImplementedError
