from signalnoise.workflow.graph import SignalNoiseGraph
from signalnoise.agents.state import SignalNoiseState

class SignalNoiseService:

    def __init__(
        self,
        graph:SignalNoiseGraph
    ):
        self.graph = graph


    def analyze(
        self,
        query: str,
        analysis_mode: str = "query",
        document_type: str | None = None,
        source: str | None = None
    ):
        state = SignalNoiseState(
            query=query,
            analysis_mode=analysis_mode,
            historical_analysis=(analysis_mode == "portfolio"),
            document_type=document_type,
            source=source
        )

        return self.graph.invoke(state)