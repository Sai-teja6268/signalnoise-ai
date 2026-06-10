from signalnoise.agents.retrieval_agent import RetrievalAgent
from signalnoise.agents.signal_agent import SignalAgent
from signalnoise.agents.trend_agent import TrendAgent
from signalnoise.agents.risk_agent import RiskAgent
from signalnoise.agents.summary_agent import SummaryAgent
from signalnoise.retrieval.hybrid_retrieval import HybridRetriever
from signalnoise.signals.llm_signal_detector import LLMSignalDetector
from signalnoise.trends.trend_detector import TrendDetector
from signalnoise.risk.risk_engine import RiskEngine
from signalnoise.executive_summary.executive_summary_generator import ExecutiveSummaryGenerator

class AgentsFactory:
    @staticmethod
    def create_retrieval_agent(chunks):
        return RetrievalAgent(HybridRetriever(chunks))

    @staticmethod
    def create_signal_agent():

        return SignalAgent(
            LLMSignalDetector()
        )

    @staticmethod
    def create_trend_agent():
        from signalnoise.history.trend_analyzer import TrendAnalyzer
        from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
        from signalnoise.repository.postgres_trend_repository import PostgresTrendRepository

        return TrendAgent(
            trend_analyzer=TrendAnalyzer(),
            signal_repo=PostgresSignalRepository(),
            trend_repo=PostgresTrendRepository()
        )

    @staticmethod
    def create_risk_agent():
        from signalnoise.repository.postgres_risk_repository import PostgresRiskRepository
        from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository

        return RiskAgent(
            risk_engine=RiskEngine(),
            risk_repo=PostgresRiskRepository(),
            signal_repo=PostgresSignalRepository()
        )

    @staticmethod
    def create_summary_agent():

        return SummaryAgent(
            ExecutiveSummaryGenerator()
        )

    @staticmethod
    def create_history_agent():
        from signalnoise.agents.history_agent import HistoryAgent
        from signalnoise.repository.postgres_signal_repository import PostgresSignalRepository
        return HistoryAgent(PostgresSignalRepository())

    @staticmethod
    def create_forecast_agent():
        from signalnoise.forecasting.forecast_agent import ForecastAgent
        from signalnoise.forecasting.forecast_engine import ForecastEngine
        return ForecastAgent(ForecastEngine())

