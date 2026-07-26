import logging


logger = logging.getLogger(__name__)


class FraudDetector:
    """
    FSE P2P Security Layer

    Responsibilities:
    - Analyze transaction risk signals
    - Detect suspicious patterns
    - Provide risk assessment

    Does NOT:
    - Confirm bank payments
    - Release USDT
    - Replace real banking verification
    """

    def __init__(
        self,
        max_risk_score=70
    ):
        self.max_risk_score = max_risk_score


    def analyze(
        self,
        payment_data: dict
    ) -> dict:
        """
        Analyze payment information.

        Returns risk assessment only.
        """

        risk_score = 0
        reasons = []

        if not payment_data:
            return {
                "approved": False,
                "risk_score": 100,
                "reasons": [
                    "Missing payment data"
                ]
            }


        transaction_count = payment_data.get(
            "recent_transactions",
            0
        )

        if transaction_count > 20:
            risk_score += 30
            reasons.append(
                "High transaction frequency"
            )


        account_age = payment_data.get(
            "account_age_days",
            0
        )

        if account_age < 7:
            risk_score += 25
            reasons.append(
                "New account"
            )


        failed_attempts = payment_data.get(
            "failed_attempts",
            0
        )

        if failed_attempts > 3:
            risk_score += 30
            reasons.append(
                "Multiple failed attempts"
            )


        approved = (
            risk_score < self.max_risk_score
        )


        return {
            "approved": approved,
            "risk_score": risk_score,
            "reasons": reasons
        }
