import logging


logger = logging.getLogger(__name__)


class MerchantScoring:
    """
    FSE P2P Merchant Reputation Engine

    Responsibilities:
    - Evaluate merchant risk
    - Calculate trust score
    - Provide decision support

    Does NOT:
    - Approve payments
    - Release USDT
    - Create fake reputation
    """

    def __init__(self):
        pass

    def calculate_score(
        self,
        merchant: dict
    ) -> float:

        score = 0.0

        successful = merchant.get(
            "successful_trades",
            0
        )

        failed = merchant.get(
            "failed_trades",
            0
        )

        disputes = merchant.get(
            "disputes",
            0
        )

        if successful > 0:
            score += min(
                successful,
                50
            )

        if failed == 0:
            score += 20

        if disputes == 0:
            score += 20

        account_age = merchant.get(
            "account_age_days",
            0
        )

        if account_age > 30:
            score += 10

        return float(
            min(
                score,
                100
            )
        )

    def is_trusted(
        self,
        merchant: dict,
        minimum_score=70
    ) -> bool:

        score = self.calculate_score(
            merchant
        )

        return score >= minimum_score
