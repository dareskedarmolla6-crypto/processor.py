from market.market_data_application import MarketDataApplication
from market.market_data_orchestrator import MarketDataOrchestrator
from market.market_data_supervisor import MarketDataSupervisor
from market.market_data_runtime import MarketDataRuntime


class MarketDataContainer:
    """
    Production dependency composition root.

    Creates and wires market data components.

    Does NOT contain:
        - Market data logic
        - Exchange communication
        - Trading decisions
    """

    def __init__(self, scheduler):

        runtime = MarketDataRuntime(
            scheduler
        )

        supervisor = MarketDataSupervisor(
            runtime
        )

        orchestrator = MarketDataOrchestrator(
            supervisor
        )

        self.application = MarketDataApplication(
            orchestrator
        )
