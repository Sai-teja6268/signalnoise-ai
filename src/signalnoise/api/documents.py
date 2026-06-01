from fastapi import APIRouter
from signalnoise.services.ingestion_service import IngestionService

router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.post("/ingest/{file_path}")
def ingest_document(file_path:str):
    ingestion_service = IngestionService()
    documents = ingestion_service.ingest(file_path)
    return documents
