import os
import shutil
import tempfile
from typing import Optional
from fastapi import APIRouter, File, Form, UploadFile, HTTPException
from signalnoise.services.ingestion_service import IngestionService
from signalnoise.document_registry.document_service import DocumentRegistryService


router = APIRouter(
    prefix="/documents",
    tags=["documents"]
)

@router.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    source: Optional[str] = Form(
        default=None,
        description=(
            "Business origin of the document. "
            "Valid values: jira, confluence, slack, meeting_notes, email, support, incident, retrospective, delivery, compliance. "
            "When omitted, source is auto-detected from filename and content."
        )
    ),
    document_type: Optional[str] = Form(
        default=None,
        description=(
            "Semantic category of the document. "
            "Valid values: support, incident, retrospective, delivery, compliance, security, operations. "
            "When omitted, document_type is auto-classified from filename and content."
        )
    ),
):
    """Ingest a document file into the SignalNoise knowledge base.

    - **file**: The document to upload (.txt, .csv, .pdf, etc.)
    - **source**: Optional explicit source system (e.g. `jira`, `support`).
    - **document_type**: Optional explicit document category (e.g. `incident`, `delivery`).
    """
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Construct path using safe original filename
        filename = os.path.basename(file.filename)
        temp_file_path = os.path.join(temp_dir, filename)

        # Save file to temp directory
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        ingestion_service = IngestionService()
        try:
            documents = ingestion_service.ingest(
                file_path=temp_file_path,
                source=source or None,
                document_type=document_type or None,
            )
            return documents
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
    finally:
        # Clean up temporary directory and files
        shutil.rmtree(temp_dir)


@router.get("")
async def get_all_documents():
    service = DocumentRegistryService()
    return service.get_all_documents()


@router.get("/{document_id}")
async def get_document_by_id(document_id: str):
    service = DocumentRegistryService()
    doc = service.get_document_by_id(document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


