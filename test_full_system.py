from brain.alpha_universe import AlphaUniverse
from brain.volatility_engine import VolatilityEngine
from brain.trend_engine import TrendEngine
from brain.reversal_engine import ReversalEngine
# ትክክለኛው የፋይል ስም imports
from brain.risk_engine import RiskEngine 
from brain.leverage_engine import LeverageEngine
from brain.grid_engine import GridEngine
from brain.predictor import Predictor
from brain.execution_engine import ExecutionEngine
from brain.signal_engine import SignalEngine
from brain.auto_scanner import AutoScanner
from brain.portfolio_engine import PortfolioEngine
from brain.exit_strategy import ExitStrategy
from brain.position_manager import PositionManager
from brain.full_system import FullSystem

def run_test():
    # 1. Initialize Engines
    alpha = AlphaUniverse()
    volatility = VolatilityEngine()
    trend = TrendEngine()
    reversal = ReversalEngine()
    
    # ትክክለኛው የRiskEngine initialization
    risk = RiskEngine(max_drawdown=30, max_leverage=40, max_risk_per_trade=0.03)
    
    leverage = LeverageEngine()
    grid = GridEngine()
    predictor = Predictor()
    execution = ExecutionEngine()
    signal_engine = SignalEngine()
    scanner = AutoScanner(alpha=alpha, signal_engine=signal_engine)
    portfolio = PortfolioEngine()
    exit_strat = ExitStrategy()

    # Position Manager Initialization
    position_manager = PositionManager(
        execution=execution, 
        smart_exit=exit_strat, 
        risk_engine=risk
    )

    # 2. Initialize FullSystem
    system = FullSystem(
        alpha=alpha, volatility=volatility, trend=trend, reversal=reversal,
        risk=risk, leverage=leverage, grid=grid, predictor=predictor,
        execution=execution, signal_engine=signal_engine, scanner=scanner,
        portfolio_engine=portfolio, position_manager=position_manager
    )

    # 3. Multi-Coin Mock Data
    market_data = {
        "COIN_A": {"price": 100, "volatility": 8, "volume": 50000, "trend": 1},
        "COIN_B": {"price": 200, "volatility": 22, "volume": 800000, "trend": 6},
        "COIN_C": {"price": 50, "volatility": 35, "volume": 1500000, "trend": 8}
    }

    print("--- Running FSE Multi-Coin Opportunity Scan (Risk-Integrated) ---")

    # 4. Scanner ራሱ ይምረጥ
    scan_result = scanner.scan(market_data)
    print("Scanner Selected:", scan_result)

    if isinstance(scan_result, dict):
        selected_symbol = scan_result["symbol"]
        market = market_data[selected_symbol]

        # 5. Execute Trade
        result = system.run(market, selected_symbol, balance=1000, stop_loss_price=49)
        
        print("\nTrade Execution Result:")
        print(result)
        print("\nOpen Positions:", execution.positions)
    else:
        print("No viable opportunity found.")

if __name__ == "__main__":
    run_test()
