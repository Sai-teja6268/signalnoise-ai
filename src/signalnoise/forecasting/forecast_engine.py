from signalnoise.forecasting.forecast_model import (
    Forecast
)

from signalnoise.risk.risk_model import (
    Risk
)


class ForecastEngine:

    def forecast(
        self,
        risk: Risk
    ) -> Forecast:

        current = risk.risk_score

        predicted_7 = min(
            current * 1.05,
            100
        )

        predicted_30 = min(
            current * 1.15,
            100
        )

        if predicted_30 >= 90:

            recommendation = (
                "Immediate leadership intervention required"
            )

        elif predicted_30 >= 70:

            recommendation = (
                "Monitor closely and mitigate"
            )

        else:

            recommendation = (
                "Risk currently under control"
            )

        return Forecast(
            signal_type=risk.signal_type,
            current_risk=current,
            predicted_risk_7_days=round(predicted_7, 2),
            predicted_risk_30_days=round(predicted_30, 2),
            recommendation=recommendation
        )