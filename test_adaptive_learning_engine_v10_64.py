from datetime import datetime, UTC


class LearningMemoryV10_64:
    """
    FSE Production Learning Memory V10.64

    Responsibilities
    ----------------
    - Store real learning events
    - Keep reward history
    - Provide learning statistics

    Does NOT contain
    ----------------
    - Fake experiences
    - Simulated trades
    - Decision generation
    """


    def __init__(
        self
    ):

        self.events = []


    def record(
        self,
        learning_event: dict
    ):

        if not learning_event:
            raise ValueError(
                "Learning event required"
            )


        event = {
            **learning_event,
            "recorded_at": datetime.now(
                UTC
            ).isoformat()
        }


        self.events.append(
            event
        )


        return event



    def summary(
        self
    ):

        total = len(
            self.events
        )


        positive = sum(
            1
            for event in self.events
            if event.get("reward", 0) > 0
        )


        negative = sum(
            1
            for event in self.events
            if event.get("reward", 0) < 0
        )


        return {
            "total_events": total,
            "positive_events": positive,
            "negative_events": negative
        }
