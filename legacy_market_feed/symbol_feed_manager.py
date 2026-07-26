from market.symbol_registry import SymbolRegistry
from market.market_feed_scheduler import MarketFeedScheduler


class SymbolFeedManager:
    """
    Production symbol feed coordinator.

    Responsibilities:
    - Read symbols from registry
    - Trigger market feed scheduler

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    - Exchange communication
    """

    def __init__(
        self,
        registry: SymbolRegistry,
        scheduler: MarketFeedScheduler
    ):
        self.registry = registry
        self.scheduler = scheduler


    def run_feed_cycle(self) -> None:
        """
        Run one market feed update cycle.
        """

        symbols = self.registry.symbols()

        if not symbols:
            raise ValueError(
                "No symbols available in registry"
            )

        self.scheduler.run_cycle(
            symbols
        )
