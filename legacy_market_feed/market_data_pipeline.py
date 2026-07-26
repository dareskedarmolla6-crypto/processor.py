from models.symbol_state import SymbolState
from market.market_manager import MarketManager


class MarketDataPipeline:
    """
    Production market data update pipeline.

    Responsibilities:
    - Receive validated market states
    - Forward updates to MarketManager

    Does NOT contain:
    - Trading decisions
    - Strategy logic
    - Risk logic
    - Exchange communication
    """

    def __init__(
        self,
        market_manager: MarketManager
    ):
        self.market_manager = market_manager


    def process(
        self,
        state: SymbolState
    ) -> None:
        """
        Process validated market state.
        """

        if not isinstance(
            state,
            SymbolState
        ):
            raise TypeError(
                "Expected SymbolState"
            )

        self.market_manager.update_market_state(
            state
        )
