# fse/utils/math_utils.py

import math

from config.constants import (
    MIN_LEVERAGE,
    MAX_LEVERAGE,
    CONFIDENCE_THRESHOLD,
    LEVERAGE_LEVELS,
)

# =========================
# MATHEMATICAL UTILITIES
# =========================


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Limit value inside a safe range."""
    return max(min_val, min(value, max_val))


def safe_div(a: float, b: float, default: float = 0.0) -> float:
    """Safe division avoiding zero division."""
    return a / b if b != 0 else default


def pct_change(old: float, new: float) -> float:
    """Calculate percentage change."""
    return ((new - old) / old * 100) if old != 0 else 0.0


# =========================
# TRADING DYNAMICS
# =========================


def position_size(
    balance: float,
    risk_pct: float,
    confidence: float
) -> float:
    """
    Dynamic capital allocation based on confidence.
    """

    confidence_factor = clamp(
        confidence / 100,
        0.1,
        1.0
    )

    base = balance * (risk_pct / 100)

    return base * confidence_factor



def leverage_by_confidence(confidence: float) -> int:
    """
    FSE V11.77 Adaptive Leverage System.

    Confidence below 40:
    No directional leverage.

    Confidence 40-100:
    Uses production leverage map.
    """

    try:
        confidence = float(confidence)
    except (ValueError, TypeError):
        return MIN_LEVERAGE


    if confidence < CONFIDENCE_THRESHOLD:
        return MIN_LEVERAGE


    for (low, high), leverage in LEVERAGE_LEVELS.items():

        if low <= confidence <= high:
            return min(leverage, MAX_LEVERAGE)


    return MIN_LEVERAGE



def volatility_score(prices: list) -> float:
    """
    Market volatility estimation.
    """

    if len(prices) < 2:
        return 0.0

    changes = [
        abs(prices[i] - prices[i - 1])
        for i in range(1, len(prices))
    ]

    return sum(changes) / len(changes)



def risk_score(
    confidence: float,
    volatility: float
) -> float:
    """
    Combined risk score.
    """

    return clamp(
        confidence - (volatility * 10),
        0,
        100
    )
