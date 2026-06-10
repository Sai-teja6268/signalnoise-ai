from signalnoise.agents.agents_factory import AgentsFactory
from signalnoise.agents.retrieval_agent import RetrievalAgent
from signalnoise.agents.signal_agent import SignalAgent
from signalnoise.agents.trend_agent import TrendAgent
from signalnoise.agents.risk_agent import RiskAgent
from signalnoise.agents.summary_agent import SummaryAgent
from signalnoise.agents.history_agent import HistoryAgent
from signalnoise.forecasting.forecast_agent import ForecastAgent
from langchain_core.documents import Document

def test_agents_factory():
    # Test create_retrieval_agent
    retrieval_agent = AgentsFactory.create_retrieval_agent([
        Document(page_content="test", metadata={"source": "test", "document_id": "1", "chunk_id": "1"})
    ])
    assert isinstance(retrieval_agent, RetrievalAgent)

    # Test create_signal_agent
    signal_agent = AgentsFactory.create_signal_agent()
    assert isinstance(signal_agent, SignalAgent)

    # Test create_trend_agent
    trend_agent = AgentsFactory.create_trend_agent()
    assert isinstance(trend_agent, TrendAgent)

    # Test create_risk_agent
    risk_agent = AgentsFactory.create_risk_agent()
    assert isinstance(risk_agent, RiskAgent)

    # Test create_summary_agent
    summary_agent = AgentsFactory.create_summary_agent()
    assert isinstance(summary_agent, SummaryAgent)

    # Test create_history_agent
    history_agent = AgentsFactory.create_history_agent()
    assert isinstance(history_agent, HistoryAgent)

    # Test create_forecast_agent
    forecast_agent = AgentsFactory.create_forecast_agent()
    assert isinstance(forecast_agent, ForecastAgent)

