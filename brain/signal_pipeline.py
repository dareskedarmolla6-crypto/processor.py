from brain.market_scanner import MarketScanner
from brain.adaptive_brain import AdaptiveBrain


class SignalPipeline:
    """
    FSE Signal Pipeline

    Market
        ↓
    Scanner
        ↓
    Adaptive Brain
        ↓
    Final Signals
    """

    def __init__(
        self,
        performance_memory,
        min_confidence=0.70
    ):

        self.scanner = MarketScanner(
            min_confidence=min_confidence
        )

        self.brain = AdaptiveBrain(
            performance_memory
        )

    def process(
        self,
        market_data
    ):

        scanned = self.scanner.scan(
            market_data
        )

        decisions = []

        for signal in scanned:

            result = self.brain.evaluate(
                signal
            )

            decisions.append(
                result
            )

        return decisions
