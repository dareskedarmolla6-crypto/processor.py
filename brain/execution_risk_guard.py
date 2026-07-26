# fse/brain/execution_risk_guard.py

import logging

logger = logging.getLogger(__name__)


class ExecutionRiskGuard:
    """
    FSE Execution Risk Validation Layer.

    Responsibilities:
    - Validate execution parameters
    - Check risk approval before execution
    - Protect execution pipeline
    - Provide production-grade decision output
    """


    def __init__(self, risk_engine, telemetry=None):

        self._risk_engine = risk_engine
        self._telemetry = telemetry



    def check(
        self,
        symbol,
        size,
        price,
        confidence=None,
        leverage=None
    ):

        # Symbol validation
        if not symbol:

            return {
                "approved": False,
                "reason": "INVALID_SYMBOL"
            }



        # Execution parameter validation
        if size <= 0 or price <= 0:

            logger.warning(
                "Invalid execution parameters: %s %s %s",
                symbol,
                size,
                price
            )

            # Keep existing FSE test contract
            return "INVALID_PARAMS"



        try:

            approved = self._risk_engine.approve(
                symbol,
                size,
                price
            )


        except Exception as error:

            logger.error(
                "Risk engine failure: %s",
                error
            )

            return {
                "approved": False,
                "symbol": symbol,
                "reason": "RISK_ENGINE_ERROR"
            }



        if not approved:

            result = {

                "approved": False,

                "symbol": symbol,

                "size": size,

                "price": price,

                "reason": "RISK_REJECTED"

            }


            self._emit(
                "RISK_REJECTED",
                result
            )


            return result




        result = {

            "approved": True,

            "symbol": symbol,

            "size": size,

            "price": price,

            "confidence": confidence,

            "leverage": leverage,

            "risk_checked": True

        }


        self._emit(
            "EXECUTION_APPROVED",
            result
        )


        return result




    def _emit(
        self,
        event,
        data
    ):

        if self._telemetry:

            try:

                self._telemetry.push(
                    event,
                    data
                )


            except Exception as error:

                logger.warning(
                    "Telemetry failure: %s",
                    error
                )
