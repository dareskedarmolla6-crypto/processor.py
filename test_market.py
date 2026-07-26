from brain.market_feed import MarketFeed
from brain.alpha_universe import AlphaUniverse

feed = MarketFeed(mode="MOCK")
alpha = AlphaUniverse()

market_data = feed.get_data()
alpha.ingest(market_data)

print(alpha.get_top_market(5))
