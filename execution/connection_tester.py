import os
import logging
import requests
from dotenv import load_dotenv
from requests.exceptions import (
    Timeout,
    ConnectionError,
    HTTPError,
    RequestException
)

load_dotenv()

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO
)


def test_api_connection():

    """
    FSE V11.77 Exchange Connection Safety Check
    """

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = "https://api.binance.com"

    if not api_key:
        logger.error("❌ BINANCE_API_KEY missing")
        return False

    if not api_secret:
        logger.error("❌ BINANCE_API_SECRET missing")
        return False

    if not base_url:
        logger.error("❌ BASE_URL missing")
        return False

    try:

        endpoint = f"{base_url}/api/v3/ping"

        response = requests.get(
            endpoint,
            timeout=10
        )

        response.raise_for_status()

        logger.info(
            "✅ Exchange server reachable"
        )

        logger.info(
            f"📡 Status Code: {response.status_code}"
        )

        return True


    except Timeout:

        logger.error(
            "⏳ Connection timeout"
        )


    except ConnectionError:

        logger.error(
            "🌐 Exchange connection failed"
        )


    except HTTPError as err:

        logger.error(
            f"⚠️ HTTP Error: {err}"
        )


    except RequestException as err:

        logger.error(
            f"❌ Request Error: {err}"
        )


    except Exception as err:

        logger.error(
            f"🔥 Unexpected Error: {err}"
        )


    return False


# ==========================================
# Manual Connection Test Runner
# ==========================================

if __name__ == "__main__":

    success = test_api_connection()

    if success:

        logger.info(
            "🟢 FSE API Connection Layer Ready!"
        )

    else:

        logger.error(
            "🔴 FSE API Connection Test Failed!"
        )
