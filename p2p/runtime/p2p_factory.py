import logging

from p2p.services.p2p_service import P2PService
from p2p.core.p2p_engine import P2PEngine

from p2p.market.offer_router import OfferRouter
from p2p.scoring.merchant_scoring import MerchantScoring
from p2p.risk.p2p_risk_controller import P2PRiskController

from p2p.security.payment_verifier import PaymentVerifier
from p2p.security.fraud_detector import FraudDetector
from p2p.security.settlement_guard import SettlementGuard
from p2p.banking.account_rotation import AccountRotationManager
from p2p.monitoring.p2p_monitor import P2PMonitor
from p2p.providers.provider_registry import ProviderRegistry


logger = logging.getLogger(__name__)


class P2PRuntime:
    """
    FSE P2P Runtime Container

    Creates production dependency graph.

    Does NOT:
    - Execute payments
    - Move funds
    - Release assets
    """

    def __init__(self):

        self.provider_registry = ProviderRegistry()
        logger.info("ProviderRegistry OK")

        self.offer_router = OfferRouter(
            provider=self.provider_registry
        )
        logger.info("OfferRouter OK")

        self.merchant_scoring = MerchantScoring()
        logger.info("MerchantScoring OK")

        self.risk_controller = P2PRiskController()
        logger.info("RiskController OK")

        self.payment_verifier = PaymentVerifier()
        logger.info("PaymentVerifier OK")

        self.fraud_detector = FraudDetector()
        logger.info("FraudDetector OK")

        self.settlement_guard = SettlementGuard(
            payment_verifier=self.payment_verifier,
            fraud_detector=self.fraud_detector,
            merchant_scoring=self.merchant_scoring
        )
        logger.info("SettlementGuard OK")

        self.account_rotation = AccountRotationManager()
        logger.info("AccountRotation OK")

        self.monitor = P2PMonitor()
        logger.info("Monitor OK")

        self.service = P2PService(
            offer_router=self.offer_router,
            merchant_scoring=self.merchant_scoring,
            risk_controller=self.risk_controller,
            payment_verifier=self.payment_verifier,
            fraud_detector=self.fraud_detector,
            settlement_guard=self.settlement_guard
        )
        logger.info("P2PService OK")

        self.engine = P2PEngine(
            offer_router=self.offer_router,
            account_rotation=self.account_rotation,
            settlement_guard=self.settlement_guard
        )
        logger.info("P2PEngine OK")

        logger.info(
            "P2P Runtime initialized"
        )


def create_p2p_runtime():

    return P2PRuntime()
