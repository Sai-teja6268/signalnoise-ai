from signalnoise.risk.risk_model import (
    Risk
)
from signalnoise.trends.trend_model import (
    Trend
)

class RiskEngine:

    severity_weight={
        "Low":20,
        "Medium":50,
        "High":80
    }
    
    def calculate_risk(
        self,
        trend:Trend,
        confidence:float,
        severity:str,
        signal_count:int
    )-> Risk:
        trend_score = min(
            abs(trend.growth_rate),100
        )

        confidence_score = confidence*100

        severity_score = self.severity_weight.get(
            severity,
            25
        )

        frequency_min = min(
            signal_count*10,
            100
        )

        final_score = (
            trend_score*0.4
            +confidence_score*0.3
            +severity_score*0.2
            +frequency_min*0.1
        )
        
        final_score = round(min(final_score,100),2)

        if final_score <= 20:
            final_severity = "Low"
        elif final_score <= 50:
            final_severity = "Medium"
        else:
            final_severity = "High"

        return Risk(
            signal_type=trend.signal_type,
            severity=final_severity,
            risk_score=final_score,
            explanation=f"Trend Growth Rate: {trend.growth_rate} (30 days)"
        )