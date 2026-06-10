from langgraph.graph import StateGraph, END
from signalnoise.agents.state import SignalNoiseState

class SignalNoiseGraph:
    def __init__(
        self,
        retrieval_agent,
        signal_agent,
        history_agent,
        trend_agent,
        risk_agent,
        forecast_agent,
        summary_agent
    ):
        workflow = StateGraph(SignalNoiseState)

        workflow.add_node("retrieval", retrieval_agent)
        workflow.add_node("signals", signal_agent)
        workflow.add_node("history", history_agent)
        workflow.add_node("trends", trend_agent)
        workflow.add_node("risks", risk_agent)
        workflow.add_node("forecast", forecast_agent)
        workflow.add_node("summary", summary_agent)

        workflow.set_entry_point("retrieval")
        workflow.add_edge("retrieval", "signals")
        workflow.add_edge("signals", "history")
        workflow.add_edge("history", "trends")
        workflow.add_edge("trends", "risks")
        workflow.add_edge("risks", "forecast")
        workflow.add_edge("forecast", "summary")
        workflow.add_edge("summary", END)

        self.app = workflow.compile()

    def invoke(self,state):
        return self.app.invoke(state)
