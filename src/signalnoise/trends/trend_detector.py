from signalnoise.trends.trend_model import Trend
from collections import Counter

class TrendDetector:
    def __init__(self):
        pass
    
    def detect_trends(self, signals):
        counts = Counter(
            signal.signal_type
            for signal in signals
        )

        trends=[]

        for signal_type, count in counts.items():
            if count >= 3:
                direction = "Increasing"
            elif count == 2:
                direction = "Stable"
            else:
                direction = "Emerging"

            trends.append(
                Trend(
                    signal_type=signal_type,
                    trend_detection=direction,
                    growth_rate=float(count),
                    explaination=f"{count} signals detected in {direction} trend"
                )
            )

        return trends
    

