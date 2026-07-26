class LeverageEngine:
    """
    FSE V11.77 Confidence Based Adaptive Leverage System
    """

    def calculate(self, confidence):

        confidence = float(confidence)

        if confidence < 40:
            return 0

        elif confidence < 50:
            return 15

        elif confidence < 60:
            return 25

        elif confidence < 70:
            return 35

        elif confidence < 80:
            return 45

        elif confidence < 90:
            return 55

        else:
            return 70
