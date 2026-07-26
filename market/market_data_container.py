import logging

from market.market_manager import MarketManager
from parsers.binance_exchange_parser import BinanceExchangeParser
from market.market_data_service import MarketDataService

from market.symbol_discovery_service import SymbolDiscoveryService
from market.market_symbol_activator import MarketSymbolActivator
from market.symbol_activation_policy import SymbolActivationPolicy

from market.market_data_bootstrap import MarketDataBootstrap
from adapters.binance_market_data_adapter import BinanceMarketDataAdapter

from market.market_data_coordinator import MarketDataCoordinator
from market.market_data_scheduler import MarketDataScheduler
from market.market_data_runtime import MarketDataRuntime
from market.market_data_supervisor import MarketDataSupervisor
from market.market_data_orchestrator import MarketDataOrchestrator
from market.market_data_application import MarketDataApplication


logger = logging.getLogger(__name__)


class MarketDataContainer:
    """
    Production Market Data Dependency Container.

    Builds complete market data infrastructure.

    Flow:

    Binance Clients
          |
          v
    Parsers
          |
          v
    Symbol Discovery
          |
          v
    Market Manager
          |
          v
    Coordinator
          |
          v
    Service
          |
          v
    Scheduler
          |
          v
    Runtime
          |
          v
    Supervisor
          |
          v
    Orchestrator
          |
          v
    Application
    """

    def __init__(
        self,
        symbol_client,
        market_client,
        repository,
        symbol_registry,
        parser,
        scheduler=None
    ):
        logger.info("Initializing Market Data Container")

        self.symbol_client = symbol_client
        self.market_client = market_client
        self.repository = repository
        self.symbol_registry = symbol_registry
        self.parser = parser

        # Manager Layer
        self.manager = MarketManager(
            repository=repository
        )

        # Discovery Layer
        self.symbol_discovery = SymbolDiscoveryService(
            client=symbol_client,
            parser=BinanceExchangeParser(),
            registry=symbol_registry,
            policy=SymbolActivationPolicy()
        )

        # Activation Layer
        self.symbol_activator = MarketSymbolActivator(
            registry=symbol_registry,
            market_client=market_client,
            parser=parser,
            manager=self.manager
        )

        # Bootstrap Layer
        self.bootstrap = MarketDataBootstrap(
            self.symbol_discovery,
            self.symbol_activator
        )

        # Adapter Layer
        self.adapter = BinanceMarketDataAdapter(
            market_client,
            parser
        )

        # Coordinator Layer
        self.coordinator = MarketDataCoordinator(
            market_client,
            self.adapter,
            self.manager
        )

        # Service Layer
        self.service = MarketDataService(
            self.coordinator
        )

        # Scheduler Layer
        if scheduler is None:
            scheduler = MarketDataScheduler(
                self.service
            )
        self.scheduler = scheduler

        # Runtime Layer
        self.runtime = MarketDataRuntime(
            scheduler=self.scheduler,
            manager=self.manager
        )

        # Supervisor Layer
        self.supervisor = MarketDataSupervisor(
            self.runtime
        )

        # Orchestration Layer
        self.orchestrator = MarketDataOrchestrator(
            self.supervisor
        )

        # Application Layer
        self.application = MarketDataApplication(
            self.orchestrator
        )
