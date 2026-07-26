import re
import logging

logger = logging.getLogger("FSE.Validators")


def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format."""
    if not isinstance(symbol, str):
        logger.error("Symbol must be a string.")
        return False

    if not re.match(r"^[A-Z0-9]{5,15}$", symbol):
        logger.error(f"Invalid symbol format: {symbol}")
        return False

    return True


def validate_side(side: str) -> bool:
    """Validate trading direction."""
    if side not in ["LONG", "SHORT", "HEDGE"]:
        logger.error(f"Invalid side: {side}")
        return False

    return True


def validate_quantity(qty: float) -> bool:
    """Validate order quantity safety."""
    try:
        q = float(qty)

        if 0 < q <= 1_000_000:
            return True

        logger.error(f"Quantity out of bounds: {q}")

    except (ValueError, TypeError):
        logger.error("Quantity must be numeric.")

    return False


def validate_confidence(confidence: float) -> bool:
    """Validate confidence score."""
    try:
        c = float(confidence)

        if 0 <= c <= 100:
            return True

        logger.error(f"Invalid confidence: {c}")

    except (ValueError, TypeError):
        logger.error("Confidence must be numeric.")

    return False


def validate_signal(signal: dict) -> bool:
    """
    Central signal validation before execution.
    """

    if not isinstance(signal, dict):
        return False

    required = [
        "symbol",
        "side",
        "qty",
        "confidence"
    ]

    if not all(key in signal for key in required):
        logger.error("Missing required signal fields.")
        return False

    valid = (
        validate_symbol(signal["symbol"])
        and validate_side(signal["side"])
        and validate_quantity(signal["qty"])
        and validate_confidence(signal["confidence"])
    )

    if valid:
        logger.info(
            f"Signal validated: {signal['symbol']} {signal['side']}"
        )

    return valid
