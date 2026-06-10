from fastapi import APIRouter, Depends, HTTPException
from signalnoise.api.models.analyze_request import AnalyzeRequest
from signalnoise.api.models.analyze_response import AnalyzeResponse
from signalnoise.services.signalnoise_service import SignalNoiseService
from signalnoise.agents.agents_factory import AgentsFactory
from signalnoise.workflow.graph import SignalNoiseGraph
from signalnoise.rag.vectorstore import VectorStore
from signalnoise.rag.chunking_service import ChunkingService
from langchain_core.documents import Document
from signalnoise.observability.logger import logger

router = APIRouter(
    prefix="/analyze",
    tags=["analysis"]
)

def get_signalnoise_service() -> SignalNoiseService:
    try:
        vectorstore = VectorStore()
        chroma_client = vectorstore.get_vectorstore()
        data = chroma_client.get()
        
        documents = []
        if data and "documents" in data:
            for content, metadata in zip(data["documents"], data["metadatas"]):
                documents.append(Document(page_content=content, metadata=metadata or {}))
                
        chunks = documents
        
        # Prevent BM25 cold-start crash
        if not chunks:
            chunks = [Document(page_content="seed document", metadata={"source": "seed"})]
            
        retrieval_agent = AgentsFactory.create_retrieval_agent(chunks)
        signal_agent = AgentsFactory.create_signal_agent()
        history_agent = AgentsFactory.create_history_agent()
        trend_agent = AgentsFactory.create_trend_agent()
        risk_agent = AgentsFactory.create_risk_agent()
        forecast_agent = AgentsFactory.create_forecast_agent()
        summary_agent = AgentsFactory.create_summary_agent()

        graph = SignalNoiseGraph(
            retrieval_agent=retrieval_agent,
            signal_agent=signal_agent,
            history_agent=history_agent,
            trend_agent=trend_agent,
            risk_agent=risk_agent,
            forecast_agent=forecast_agent,
            summary_agent=summary_agent
        )
        return SignalNoiseService(graph)
    except Exception as e:
        logger.error(f"Failed to initialize SignalNoiseService: {e}")
        raise HTTPException(status_code=500, detail="Service initialization failed")

@router.post("", response_model=AnalyzeResponse)
def analyze_query(
    request: AnalyzeRequest,
    service: SignalNoiseService = Depends(get_signalnoise_service)
):
    logger.info(f"API received analysis request for query: {request.query} with mode: {request.analysis_mode}")
    try:
        result = service.analyze(
            query=request.query,
            analysis_mode=request.analysis_mode,
            document_type=request.document_type,
            source=request.source
        )
        return result
    except Exception as e:
        logger.error(f"API analysis failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
