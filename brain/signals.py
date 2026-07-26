# ==========================================================
# CONFIDENCE → LEVERAGE MAP
# FSE V11.77 Adaptive System
# ==========================================================

def calculate_leverage(confidence: int, volatility: float) -> int:
    confidence = float(confidence)

    if confidence < 40:
        return 0

    elif confidence < 50:
        base = 15

    elif confidence < 60:
        base = 25

    elif confidence < 70:
        base = 35

    elif confidence < 80:
        base = 45

    elif confidence < 90:
        base = 55

    else:
        base = 70

    # Volatility / Market Safety Adjustment
    # Alpha coins 15%+ volatility በላይ የሚመጡ ቢሆንም
    # ከፍተኛ volatility ላይ leverage እንዲቀንስ ጥበቃ

    if volatility > 0.8:
        base = int(base * 0.8)

    elif volatility > 0.6:
        base = int(base * 0.9)

    return max(base, 0)
