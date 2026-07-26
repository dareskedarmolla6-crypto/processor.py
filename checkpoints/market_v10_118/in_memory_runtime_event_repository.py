from .runtime_event_repository import RuntimeEventRepository


class InMemoryRuntimeEventRepository(
    RuntimeEventRepository
):
    """
    In-memory runtime event repository.

    Used for:
        - Testing
        - Development
        - Fast runtime validation

    Does NOT:
        - Persist to disk
        - Use database
    """

    def __init__(self):
        self._events = []

    def save_event(
        self,
        event: str
    ) -> None:

        self._events.append(
            event
        )

    def load_events(
        self
    ) -> list:

        return self._events.copy()
