import os


class P2PConfig:
    """
    FSE P2P Production Configuration

    Stores operational limits and safety parameters.

    Does NOT:
    - Execute trades
    - Approve payments
    - Verify users
    """


    # Capital management
    MAX_CAPITAL_USDT = float(
        os.getenv(
            "P2P_MAX_CAPITAL_USDT",
            "3000"
        )
    )


    # Maximum USDT sell volume per day
    DAILY_SELL_LIMIT_USDT = float(
        os.getenv(
            "P2P_DAILY_SELL_LIMIT_USDT",
            "1000"
        )
    )


    # Minimum amount allowed for one sell
    MIN_SELL_AMOUNT_USDT = float(
        os.getenv(
            "P2P_MIN_SELL_AMOUNT_USDT",
            "10"
        )
    )


    # Price safety
    MIN_PRICE_MARGIN = float(
        os.getenv(
            "P2P_MIN_PRICE_MARGIN",
            "0.98"
        )
    )


    # Merchant risk
    MAX_MERCHANT_VOLUME = float(
        os.getenv(
            "P2P_MAX_MERCHANT_VOLUME",
            "5000"
        )
    )


    # Bank account rotation
    MAX_ACCOUNT_DAILY_USAGE = float(
        os.getenv(
            "P2P_MAX_ACCOUNT_USAGE",
            "500"
        )
    )


    @classmethod
    def summary(cls):

        return {
            "max_capital": cls.MAX_CAPITAL_USDT,
            "daily_sell_limit": cls.DAILY_SELL_LIMIT_USDT,
            "min_sell_amount": cls.MIN_SELL_AMOUNT_USDT,
            "price_margin": cls.MIN_PRICE_MARGIN,
            "merchant_limit": cls.MAX_MERCHANT_VOLUME,
            "account_limit": cls.MAX_ACCOUNT_DAILY_USAGE,
        }
