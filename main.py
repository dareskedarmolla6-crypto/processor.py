import logging
import atexit

from brain.full_system import FullSystem
from brain.alpha_universe import AlphaUniverse
from brain.volatility_engine import VolatilityEngine
from brain.trend_engine import TrendEngine
from brain.reversal_engine import ReversalEngine
from brain.risk_engine import RiskEngine
from brain.leverage_engine import LeverageEngine
from brain.grid_engine import GridEngine
from brain.predictor import Predictor
from brain.execution_engine import ExecutionEngine

from brain.signal_engine import SignalEngine
from brain.auto_scanner import AutoScanner
from brain.portfolio_engine import PortfolioEngine
from brain.position_manager import PositionManager
from brain.exit_strategy import ExitStrategy
from market.container_factory import create_market_container
from brain.v12_autonomous_runtime_governance_foundation import (
    AutonomousRuntimeGovernanceFoundationV12
)

from clients.binance_futures_client import BinanceFuturesClient
from execution.execution_engine import (
    BinanceGateway,
    ExecutionCoordinator
)
from execution.execution_adapter import ExecutionAdapter
from data.storage import InMemoryStore

from p2p.runtime.p2p_factory import create_p2p_runtime


class RuntimeGovernanceOrchestrator:
    def orchestrate_execution(self):

        return {
            "decision": "ALLOW"
        }


logger = logging.getLogger("FSE")


def create_system(market_manager):

    alpha = AlphaUniverse()
    volatility = VolatilityEngine()
    trend = TrendEngine()
    reversal = ReversalEngine()

    risk = RiskEngine()
    leverage = LeverageEngine()
    grid = GridEngine()

    predictor = Predictor()
    execution = ExecutionEngine()

    futures_client = BinanceFuturesClient()

    gateway = BinanceGateway(
        futures_client
    )

    store = InMemoryStore()
    store.load_from_file()
    atexit.register(store.safe_save_to_file)

    execution_coordinator = ExecutionCoordinator(
        risk_engine=risk,
        gateway=gateway,
        store=store
    )

    execution_adapter = ExecutionAdapter(
        execution_coordinator
    )

    execution.exchange_executor = execution_adapter

    signal_engine = SignalEngine()

    scanner = AutoScanner(
        alpha=alpha,
        signal_engine=signal_engine
    )

    portfolio_engine = PortfolioEngine()

    exit_strategy = ExitStrategy()

    position_manager = PositionManager(
        execution=execution,
        smart_exit=exit_strategy,
        risk_engine=risk,
        exchange_execution=execution_coordinator
    )

    return FullSystem(
        alpha=alpha,
        volatility=volatility,
        trend=trend,
        reversal=reversal,
        risk=risk,
        leverage=leverage,
        grid=grid,
        predictor=predictor,
        execution=execution,
        signal_engine=signal_engine,
        scanner=scanner,
        portfolio_engine=portfolio_engine,
        position_manager=position_manager,
        market_manager=market_manager
    )


def main():
    logger.info(
        "Starting FSE Production Runtime"
    )

    # Real market infrastructure
    market_container = create_market_container()

    # Initialize real symbol discovery and activation
    market_container.bootstrap.initialize()

    # Start market data runtime
    market_container.application.start()

    p2p_runtime = create_p2p_runtime()

    logger.info(
        "P2P Production Runtime Ready"
    )

    system = create_system(
        market_container.manager
    )

    runtime = AutonomousRuntimeGovernanceFoundationV12(
        runtime_supervisor=market_container.supervisor,
        execution_controller=system.execution,
        orchestrator=RuntimeGovernanceOrchestrator(),
        full_system=system
    )

    runtime.start_runtime()

    logger.info(
        "FSE Production System Ready"
    )

    return runtime


if __name__ == "__main__":
    main()
