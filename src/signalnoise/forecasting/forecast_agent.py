from signalnoise.forecasting.forecast_model import (
    Forecast
)

from signalnoise.risk.risk_model import (
    Risk
)

from signalnoise.forecasting.forecast_engine import (
    ForecastEngine
)
from signalnoise.observability.logger import logger


class ForecastAgent:
    def __init__(
        self,
        forecast_engine: ForecastEngine
    ):
        self.forecast_engine = forecast_engine

    def _run_forecast(
        self,
        state
    ):
        is_dict = isinstance(state, dict)
        risks = state["risks"] if is_dict else state.risks

        forecasts = []

        for risk in risks:

            forecast = self.forecast_engine.forecast(risk)
            forecasts.append(forecast)

        logger.info(
            f"Generated {len(forecasts)} forecasts"
        )

        if is_dict:
            state["forecasts"] = forecasts
        else:
            state.forecasts = forecasts

        return state


    def __call__(
        self,
        state
    ):
        return self._run_forecast(state)