# ==========================================================
# FSE GLOBAL SETTINGS (OPERATIONAL CONFIG)
# ==========================================================
import logging

logger = logging.getLogger(__name__)

class Settings:
    """የቦቱን የስራ መቼቶች የሚቆጣጠር ክፍል (መርህ #7 & #8)"""

    # Market Scan Interval (3 ደቂቃ - መርህ #6)
    INTERVAL = 180

    # ከፍተኛ የአንድ ጊዜ ክፍት ቦታዎች (መርህ #9)
    MAX_OPEN_POSITIONS = 20

    # Minimum confidence (መርህ #4) - ወደ 40 አድጓል
    CONFIDENCE_THRESHOLD = 40

    # Trading mode
    MODE = "ALPHA_ONLY"

    # Focus only on high volatility coins (መርህ #4)
    MIN_VOLATILITY_PERCENT = 15

    # Supported trading styles - መስመሩ ተስተካክሏል
    ENABLE_LONG = True
    ENABLE_SHORT = True
    ENABLE_HEDGE = True
    ENABLE_GRID = True

    # Leverage limits (መርህ #8) - ከ 0 እስከ 70x እንዲሆን ተደርጓል
    MIN_LEVERAGE = 0
    MAX_LEVERAGE = 70

    # FSE V11.77 confidence-based leverage map
    LEVERAGE_LEVELS = {
        (40, 49): 15,
        (50, 59): 25,
        (60, 69): 35,
        (70, 79): 45,
        (80, 89): 55,
        (90, 100): 70
    }

def validate_settings():
    """የመቼቶች መጣጣምን ማረጋገጥ።"""
    # የሊቨሬጅ ወሰን ቫሊዴሽን ወደ 0 እና 70 ተቀይሯል
    if Settings.MIN_LEVERAGE < 0 or Settings.MAX_LEVERAGE > 70:
        logger.error("🚨 Configuration Error: Leverage out of safe bounds.")
        return False
    
    # የኮንፊደንስ ወሰን ቫሊዴሽን ወደ 40 ተቀይሯል
    if Settings.CONFIDENCE_THRESHOLD < 40:
        logger.warning("⚠️ Low confidence threshold detected.")
        
    logger.info("✅ FSE Settings validated successfully.")
    return True

# አጠቃላይ የመቼት መጫኛ አፈጻጸም
validate_settings()
