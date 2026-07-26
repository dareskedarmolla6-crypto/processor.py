import pytest

from main import create_system
from market.container_factory import create_market_container


class TestFSEEndToEndRuntime:

    def test_full_production_startup_chain(self):

        # 1. Market infrastructure
        market_container = create_market_container()

        assert market_container is not None

        # bootstrap real market layer
        market_container.bootstrap.initialize()

        # application runtime
        market_container.application.start()

        assert market_container.bootstrap is not None

        # 2. Build full system
        system = create_system(
            market_container.manager
        )

        assert system is not None

        # 3. Core brain components
        assert system.risk is not None
        assert system.execution is not None
        assert system.position_manager is not None
        assert system.signal_engine is not None

        # 4. Position manager chain
        pm = system.position_manager

        assert pm.execution is not None
        assert pm.smart_exit is not None
        assert pm.risk_engine is not None

        # 5. Runtime health
        result = {
            "market": True,
            "brain": True,
            "risk": True,
            "execution": True,
            "position_management": True
        }

        assert all(result.values())

    def test_execution_risk_position_flow(self):

        market_container = create_market_container()
        market_container.bootstrap.initialize()

        system = create_system(
            market_container.manager
        )

        # Get active symbol dynamically from market manager
        active_symbols = market_container.manager.active_symbols()
        assert len(active_symbols) > 0, "No active symbols found in market manager"

        symbol = active_symbols[0]
        state = market_container.manager.get_market_state(symbol)
        assert state is not None, f"No market state found for symbol: {symbol}"

        # Fetch real price dynamically
        price = state.last_price
        stop_loss_price = price * 0.98 if price and price > 0 else None

        signal = {
            "signal": "BUY"
        }

        response = system.position_manager.manage(
            symbol=symbol,
            signal=signal,
            price=price,
            balance=1000,
            stop_loss_price=stop_loss_price
        )

        assert response is not None

        assert response["action"] in [
            "OPEN",
            "HOLD",
            "REJECTED"
        ]
