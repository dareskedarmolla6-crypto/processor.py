from brain.autonomous_controller_v8_8 import AutonomousControllerV8_8


class AutonomousControllerV8_9(AutonomousControllerV8_8):
    """
    FSE Autonomous Controller V8.9

    Multi-Cycle Autonomous Learning Controller
    """

    def __init__(
        self,
        brain,
        governor,
        execution
    ):
        super().__init__(
            brain,
            governor,
            execution
        )

        self.stats = {
            "cycles": 0,
            "wins": 0,
            "losses": 0
        }

    def run_cycles(self, signals, cycles=1):

        results = []

        for _ in range(cycles):

            result = self.run_cycle(signals)

            self.stats["cycles"] += 1

            if result["trades"]:
                self.stats["wins"] += len(result["trades"])
            else:
                self.stats["losses"] += 1

            results.append(result)

        return {
            "results": results,
            "statistics": self.get_statistics()
        }

    def get_statistics(self):

        total = self.stats["cycles"]

        if total == 0:
            win_rate = 0
        else:
            win_rate = round(
                self.stats["wins"] / total,
                2
            )

        return {
            "cycles": self.stats["cycles"],
            "wins": self.stats["wins"],
            "losses": self.stats["losses"],
            "win_rate": win_rate,
            "current_risk": self.risk_adapter.get_risk()
        }
