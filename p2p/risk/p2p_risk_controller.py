import logging
from datetime import datetime, UTC


logger = logging.getLogger(__name__)


class P2PRiskController:
    """
    FSE P2P Risk Controller

    Responsibilities:
    - Capital protection
    - Sell limits
    - Price safety checks
    - Market condition protection

    Does NOT:
    - Execute payments
    - Release USDT
    - Approve fake settlements
    """


    def __init__(
        self,
        max_daily_volume=3000,
        minimum_sell_price=0,
        minimum_balance=0
    ):
        self.max_daily_volume = max_daily_volume
        self.minimum_sell_price = minimum_sell_price
        self.minimum_balance = minimum_balance

        self.daily_volume = 0
        self.last_reset = datetime.now(UTC).date()


    def _reset_daily_volume(self):

        today = datetime.now(UTC).date()

        if today != self.last_reset:
            self.daily_volume = 0
            self.last_reset = today


    def validate_sell(
        self,
        amount,
        price,
        current_balance,
        market_stable=True
    ):

        self._reset_daily_volume()


        if amount <= 0:
            return False, "INVALID_AMOUNT"


        if price < self.minimum_sell_price:
            return False, "PRICE_TOO_LOW"


        if current_balance < self.minimum_balance:
            return False, "INSUFFICIENT_BALANCE"


        if not market_stable:
            return False, "MARKET_UNSTABLE"


        if (
            self.daily_volume + amount
            > self.max_daily_volume
        ):
            return False, "DAILY_LIMIT_REACHED"


        return True, "APPROVED"


    def record_sell(
        self,
        amount
    ):

        self.daily_volume += amount

        logger.info(
            f"P2P daily volume updated: {self.daily_volume}"
        )
