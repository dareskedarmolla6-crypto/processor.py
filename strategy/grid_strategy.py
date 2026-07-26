# fse/strategy/grid_strategy.py
import logging

logger = logging.getLogger(__name__)

# =========================
# GRID TRADING STRATEGY
# =========================
class GridStrategy:
    """የገበያ ዋጋዎችን በረድፍ (Grid) በመከፋፈል ንግድ የሚያካሂድ (መርህ #3)።"""

    def __init__(self, levels=5):
        self.levels = int(levels)

    def generate_levels(self, base_price, step_pct=0.5):
        """የዋጋ ደረጃዎችን (Price Levels) መፍጠር።"""
        levels = []
        base = float(base_price)
        step = float(step_pct) / 100.0

        for i in range(1, self.levels + 1):
            lower = base * (1.0 - (step * i))
            upper = base * (1.0 + (step * i))
            # ከተርሚናል የተቆረጠው መስመር እዚህ በትክክል ተሟልቷል
            levels.append({"buy": round(lower, 4), "sell": round(upper, 4)})

        return levels

    def execute(self, market_data):
        """የGrid Strategy ውሳኔ ማመንጫ።"""

        symbol = market_data.get("symbol")
        base_price = float(market_data.get("price", 0))
        base_size = float(market_data.get("base_size", 0))

        if not symbol or base_price <= 0 or base_size <= 0:
            logger.warning("⚠️ Grid Strategy: Invalid market data.")
            return {
                "strategy": "GRID",
                "action": "HOLD",
                "reason": "INVALID_DATA"
            }

        levels = self.generate_levels(base_price)

        logger.info(
            f"🕸 Grid Strategy ready: {len(levels)} levels for {symbol}."
        )

        return {
            "strategy": "GRID",
            "action": "GRID_READY",
            "symbol": symbol,
            "base_price": base_price,
            "base_size": base_size,
            "levels": levels
        }
