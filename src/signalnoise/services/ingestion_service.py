import os
from signalnoise.ingestion.loader_factory import loadFacory
from signalnoise.rag.chunking_service import ChunkingService
from signalnoise.observability.logger import logger
from signalnoise.core.config import settings
from signalnoise.rag.embedding_service import EmbeddingService
from signalnoise.rag.vectorstore import VectorStore
from signalnoise.ingestion.processor import DocumentProcessor
from signalnoise.document_registry.document_service import DocumentRegistryService


from signalnoise.core.constants import DOCUMENT_TYPES, SOURCES


def determine_document_type(file_path: str, content: str = "") -> str:
    """Auto-classify document type from file path and content keywords.

    Checks filename first (authoritative), then falls back to content keywords.
    """
    file_name = os.path.basename(file_path).lower()
    content_lower = content.lower() if content else ""

    # 1. Authoritative filename hints
    if "support" in file_name or "complaint" in file_name:
        return "support"
    if "incident" in file_name or "outage" in file_name:
        return "incident"
    if "retro" in file_name or "burnout" in file_name:
        return "retrospective"
    if "delivery" in file_name or "blocker" in file_name or "dependency" in file_name:
        return "delivery"
    if "compliance" in file_name or "audit" in file_name or "regulation" in file_name:
        return "compliance"
    if "security" in file_name or "vulnerability" in file_name or "breach" in file_name:
        return "security"
    if "operations" in file_name or "infrastructure" in file_name or "deployment" in file_name:
        return "operations"

    # 2. Content keyword hints (fallback)
    if "support" in content_lower or "complaint" in content_lower or "ticket" in content_lower or "customer satisfaction" in content_lower:
        return "support"
    if "incident" in content_lower or "outage" in content_lower or "sev-" in content_lower or "severity" in content_lower:
        return "incident"
    if "retro" in content_lower or "burnout" in content_lower or "sprint" in content_lower:
        return "retrospective"
    if "delivery" in content_lower or "blocker" in content_lower or "dependency" in content_lower or "milestone" in content_lower:
        return "delivery"
    if "compliance" in content_lower or "audit" in content_lower or "regulation" in content_lower or "policy" in content_lower:
        return "compliance"
    if "security" in content_lower or "vulnerability" in content_lower or "breach" in content_lower or "patch" in content_lower:
        return "security"
    if "operations" in content_lower or "infrastructure" in content_lower or "deployment" in content_lower:
        return "operations"

    return "unknown"


def determine_source(file_path: str, content: str = "") -> str:
    """Auto-detect the business origin (source system) of the document.

    Checks filename first (authoritative), then falls back to content keywords.
    Returns 'unknown' when no match is found.
    """
    file_name = os.path.basename(file_path).lower()
    content_lower = content.lower() if content else ""

    # 1. Authoritative filename hints
    if "jira" in file_name:
        return "jira"
    if "confluence" in file_name:
        return "confluence"
    if "slack" in file_name:
        return "slack"
    if "meeting" in file_name:
        return "meeting_notes"
    if "email" in file_name:
        return "email"
    if "support" in file_name:
        return "support"
    if "incident" in file_name:
        return "incident"

    # 2. Content keyword hints (only if filename didn't identify source)
    if any(kw in content_lower for kw in ["customer complaint", "refund request", "ticket volume", "customer satisfaction"]):
        return "support"
    if any(kw in content_lower for kw in ["incident severity", "sev-1", "sev-2", "postmortem", "on-call"]):
        return "incident"
    if any(kw in content_lower for kw in ["support", "billing", "escalation"]):
        return "support"
    if any(kw in content_lower for kw in ["incident", "outage", "downtime"]):
        return "incident"

    return "unknown"


class IngestionService:
    def __init__(
        self,
        chunker: ChunkingService = None,
        vectorstore: VectorStore = None,
        processor: DocumentProcessor = None,
        registry_service: DocumentRegistryService = None
    ):
        self.chunker = chunker or ChunkingService()
        self.vectorstore = vectorstore or VectorStore()
        self.processor = processor or DocumentProcessor()
        self.registry_service = registry_service or DocumentRegistryService()

    def ingest(
        self,
        file_path: str,
        source: str = None,
        document_type: str = None
    ):
        """Ingest a file into the vectorstore and document registry.

        Args:
            file_path: Absolute path to the file on disk.
            source: Business origin override (e.g. 'jira', 'support', 'slack').
                    When None, source is auto-detected from filename + content.
            document_type: Semantic category override (e.g. 'incident', 'delivery').
                    When None, document_type is auto-classified from filename + content.
        """
        logger.info(f"Ingesting file: {file_path}")

        # Ingestion Guard: Check for duplicate by hash
        existing = self.registry_service.check_duplicate(file_path)
        if existing:
            logger.info(f"Document already exists in registry (hash match): {existing.document_id}")
            return {
                "message": "Document already exists",
                "document_id": existing.document_id
            }

        # Clean and validate input overrides
        if isinstance(document_type, str):
            document_type = document_type.strip().lower()
            if document_type in ("string", "none", ""):
                document_type = None

        if isinstance(source, str):
            source = source.strip().lower()
            if source in ("string", "none", ""):
                source = None

        if document_type is not None and document_type not in DOCUMENT_TYPES:
            raise ValueError(
                f"Invalid document_type '{document_type}'. "
                f"Must be one of: {sorted(list(DOCUMENT_TYPES))}"
            )

        if source is not None and source not in SOURCES:
            raise ValueError(
                f"Invalid source '{source}'. "
                f"Must be one of: {sorted(list(SOURCES))}"
            )

        loader = loadFacory.get_loader(file_path)
        logger.info(f"Loaded file with {loader.__class__.__name__}")
        documents = loader.load(file_path)
        logger.info(f"Loaded {len(documents)} documents")

        # Use explicit overrides when provided; fall back to auto-detection
        content = documents[0].content if documents else ""
        if document_type is None:
            document_type = determine_document_type(file_path, content)
            logger.info(f"Auto-classified document_type: {document_type}")
        else:
            logger.info(f"Using explicit document_type: {document_type}")

        if source is None:
            source = determine_source(file_path, content)
            logger.info(f"Auto-detected source: {source}")
        else:
            logger.info(f"Using explicit source: {source}")

        # Convert EnterpriseDocument list to LangChain Document list
        processed_docs = self.processor.process_documents(documents)

        logger.info(f"Chunking {len(processed_docs)} documents")
        chunks = self.chunker.chunk_documents(processed_docs)
        logger.info(f"Generated {len(chunks)} chunks")

        # Document Registration (Step 7 / 9)
        doc_metadata = self.registry_service.register_document(
            file_path=file_path,
            chunk_count=len(chunks),
            document_type=document_type,
            source=source
        )

        # Apply correct metadata to every chunk: document_id, document_type, source, file_name
        for i, chunk in enumerate(chunks):
            chunk.metadata["document_id"] = doc_metadata.document_id
            chunk.metadata["document_type"] = doc_metadata.document_type
            chunk.metadata["source"] = doc_metadata.source
            chunk.metadata["file_name"] = doc_metadata.file_name
            chunk.metadata["chunk_id"] = f"{doc_metadata.document_id}_chunk_{i}"
            chunk.metadata["chunk_Id"] = f"{doc_metadata.document_id}_chunk_{i}"

        # Ensure documents have correct registered details
        for doc in documents:
            doc.document_id = doc_metadata.document_id
            doc.source = doc_metadata.source

        logger.info(f"Adding {len(chunks)} chunks to vectorstore")
        ids = [chunk.metadata["chunk_id"] for chunk in chunks]
        self.vectorstore.add_documents(documents=chunks, ids=ids)
        logger.info(f"Successfully ingested {len(chunks)} chunks into vectorstore")

        return documents