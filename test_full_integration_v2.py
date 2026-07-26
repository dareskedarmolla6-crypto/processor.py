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
from brain.smart_exit import SmartExit
from brain.position_manager import PositionManager
from brain.full_system import FullSystem


def run_test():

    print("========== FULL SYSTEM INTEGRATION V2 ==========")

    # Engines
    alpha = AlphaUniverse()
    volatility = VolatilityEngine()
    trend = TrendEngine()
    reversal = ReversalEngine()
    risk = RiskEngine(
        max_drawdown=30,
        max_leverage=40,
        max_risk_per_trade=0.03
    )

    leverage = LeverageEngine()
    grid = GridEngine()
    predictor = Predictor()
    execution = ExecutionEngine()
    signal_engine = SignalEngine()

    scanner = AutoScanner(
        alpha=alpha,
        signal_engine=signal_engine
    )

    portfolio = PortfolioEngine()
    smart_exit = SmartExit()

    position_manager = PositionManager(
        execution=execution,
        smart_exit=smart_exit,
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
        portfolio_engine=portfolio,
        position_manager=position_manager
    )


    # Mock Market
    market = {
        "COIN_C": {
            "price": 50,
            "volatility": 35,
            "volume": 1500000,
            "trend": 8
        }
    }


    result = system.run(
        market["COIN_C"],
        "COIN_C",
        balance=1000,
        change=2,
        stop_loss_price=49
    )


    print("\nSYSTEM RESULT:")
    print(result)


    print("\nOPEN POSITIONS:")
    print(execution.positions)


    assert result["mode"] == "MANAGED_POSITION"

    assert "COIN_C" in execution.positions

    assert execution.positions["COIN_C"][0]["status"] == "OPEN"


    print("\nFULL SYSTEM INTEGRATION PASSED ✅")


if __name__ == "__main__":
    run_test()
