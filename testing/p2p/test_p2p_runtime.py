from p2p.runtime.p2p_factory import create_p2p_runtime


class TestP2PRuntime:

    def test_runtime_creation(self):

        runtime = create_p2p_runtime()

        assert runtime is not None

        assert runtime.service is not None
        assert runtime.engine is not None

        assert runtime.offer_router is not None
        assert runtime.merchant_scoring is not None

        assert runtime.risk_controller is not None

        assert runtime.payment_verifier is not None
        assert runtime.fraud_detector is not None
        assert runtime.settlement_guard is not None

        assert runtime.account_rotation is not None
        assert runtime.monitor is not None

    def test_service_dependencies(self):

        runtime = create_p2p_runtime()

        service = runtime.service

        assert service.offer_router is runtime.offer_router

        assert service.merchant_scoring is runtime.merchant_scoring

        assert service.risk_controller is runtime.risk_controller

        assert service.payment_verifier is runtime.payment_verifier

        assert service.fraud_detector is runtime.fraud_detector

        assert service.settlement_guard is runtime.settlement_guard

    def test_engine_exists(self):

        runtime = create_p2p_runtime()

        assert runtime.engine is not None
