from repositories.market_repository import MarketRepository


def test_market_repository_contract():

    assert hasattr(MarketRepository, "save")
    assert hasattr(MarketRepository, "get")
    assert hasattr(MarketRepository, "exists")
