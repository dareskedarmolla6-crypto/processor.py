import logging

from clients.binance_client import BinanceClient

from clients.binance_symbol_client import (
    BinanceSymbolClient
)

from clients.binance_market_data_client import (
    BinanceMarketDataClient
)

from parsers.binance_market_data_parser import (
    BinanceMarketDataParser
)

from registry.symbol_registry import (
    SymbolRegistry
)

from repositories.sqlite_market_repository import (
    SQLiteMarketRepository
)

from market.market_data_container import (
    MarketDataContainer
)


logger = logging.getLogger("FSE")


def create_market_container():

    logger.info(
        "Creating Production Market Container"
    )

    binance_client = BinanceClient()


    symbol_client = BinanceSymbolClient(
        binance_client
    )


    market_client = BinanceMarketDataClient(
        binance_client
    )


    parser = BinanceMarketDataParser()


    repository = SQLiteMarketRepository(
        "fse_data.db"
    )


    symbol_registry = SymbolRegistry()


    return MarketDataContainer(
        symbol_client=symbol_client,
        market_client=market_client,
        repository=repository,
        symbol_registry=symbol_registry,
        parser=parser
    )
