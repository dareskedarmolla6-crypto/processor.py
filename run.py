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


def create_system():

    alpha = AlphaUniverse()

    volatility = VolatilityEngine()

    trend = TrendEngine()

    reversal = ReversalEngine()

    risk = RiskEngine()

    leverage = LeverageEngine()

    grid = GridEngine()

    predictor = Predictor()

    execution = ExecutionEngine()


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
        risk_engine=risk
    )


    system = FullSystem(
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
        position_manager=position_manager
    )


    return system



if __name__ == "__main__":

    system = create_system()

    print(
        "FSE Production System Initialized"
    )
