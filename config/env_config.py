import os
import logging

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class EnvConfig:
    """
    Production environment configuration.

    Handles:
        - Exchange credentials
        - External service credentials
        - Runtime environment settings
    """

    BINANCE_API_KEY = os.getenv(
        "BINANCE_API_KEY"
    )

    BINANCE_API_SECRET = os.getenv(
        "BINANCE_API_SECRET"
    )

    TELEGRAM_TOKEN = os.getenv(
        "TELEGRAM_TOKEN"
    )

    AUTHORIZED_USER = os.getenv(
        "AUTHORIZED_USER"
    )

    ENV = os.getenv(
        "ENV",
        "production"
    )

    @classmethod
    def validate(cls) -> bool:
        """
        Validate required environment variables.
        """

        required = [
            "BINANCE_API_KEY",
            "BINANCE_API_SECRET",
        ]

        missing = [
            key
            for key in required
            if not os.getenv(key)
        ]

        if missing:
            raise EnvironmentError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

        logger.info(
            "Environment validation completed successfully."
        )

        return True


EnvConfig.validate()
