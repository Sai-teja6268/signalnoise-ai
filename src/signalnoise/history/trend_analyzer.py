from datetime import datetime, timedelta
from collections import defaultdict
from signalnoise.history.signal_history import SignalHistory
from signalnoise.trends.trend_model import Trend
from signalnoise.history.signal_store import SignalStore



class TrendAnalyzer:

    def __init__(self):
        self.signal_store = SignalStore()

    def analyze_trends(self, history: list[SignalHistory]) -> list[Trend]:
        grouped = defaultdict(list)
        signals = history
        trends = []
        now = datetime.now()
        current_window = now - timedelta(days=7)
        previous_window = now - timedelta(days=14)

        for item in history:    
            grouped[item.signal_type].append(item)

        for signal_type, records in grouped.items():

            current_count =len([
                r for r in records 
                if r.detected_at >= current_window
            ])
            
            previous_count =len([
                r for r in records 
                if previous_window <=r.detected_at < current_window
            ])

            if previous_count == 0:
                growth_rate = float(current_count)
            else:
                growth_rate = (
                    (current_count - previous_count) / previous_count * 100
                )
                
            
            if growth_rate > 20:
                trend_detection="Increasing"
            elif growth_rate < -20:
                trend_detection="Decreasing"
            else:
                trend_detection = "Stable"
            
            trend = Trend(
                signal_type=signal_type,
                trend_detection=trend_detection,
                growth_rate=round(growth_rate,2),
                explaination=f"{growth_rate} signals detected"
            )
            trends.append(trend)
        return trends
        