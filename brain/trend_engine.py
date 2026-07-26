class TrendEngine:
    """
    Confirms trend changes before reversing positions.
    """

    def __init__(self, confirmation=3):
        self.confirmation = confirmation
        self.history = []

    def update(self, direction):
        """
        direction:
        "LONG"
        "SHORT"
        """

        self.history.append(direction)

        if len(self.history) > self.confirmation:
            self.history.pop(0)

    def confirmed(self):
        if len(self.history) < self.confirmation:
            return False

        return len(set(self.history)) == 1

    def current_trend(self):
        if not self.confirmed():
            return "WAIT"

        return self.history[-1]
