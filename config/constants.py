# ==========================================================
# FSE GLOBAL CONSTANTS
# V11.77 Production Configuration
# ==========================================================

# Risk Limits
MAX_RISK_PER_TRADE = 0.02
MAX_EXPOSURE = 0.30
MAX_DRAWDOWN = 0.25

# Confidence Control
CONFIDENCE_THRESHOLD = 40

# Leverage Limits
MIN_LEVERAGE = 0
MAX_LEVERAGE = 70

# Confidence Adaptive Leverage Map
LEVERAGE_LEVELS = {
    (40, 49): 15,
    (50, 59): 25,
    (60, 69): 35,
    (70, 79): 45,
    (80, 89): 55,
    (90, 100): 70
}

# Portfolio
MAX_OPEN_POSITIONS = 20

# Market
MARKET_SCAN_INTERVAL = 180

# Trading Modes
ENABLE_LONG = True
ENABLE_SHORT = True
ENABLE_HEDGE = True
ENABLE_GRID = True


def validate_constants():
    """
    Production configuration validation
    """

    if MIN_LEVERAGE < 0:
        raise ValueError("Invalid minimum leverage")

    if MAX_LEVERAGE > 70:
        raise ValueError("Maximum leverage exceeds production limit")

    if CONFIDENCE_THRESHOLD < 40:
        raise ValueError("Confidence threshold too low")

    return True





