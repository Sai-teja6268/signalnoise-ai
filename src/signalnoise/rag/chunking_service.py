from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from typing import List
from signalnoise.ingestion.schema import EnterpriseDocument
class ChunkingService:
    def __init__(self, chunk_size=500, chunk_overlap=100):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        all_chunks = []
        for doc in documents:
            chunks = self.text_splitter.split_documents([doc])
            for i, chunk in enumerate(chunks):
                doc_id = chunk.metadata.get("document_id", "unknown")
                chunk.metadata["chunk_id"] = f"{doc_id}_chunk_{i}"
                chunk.metadata["chunk_Id"] = f"{doc_id}_chunk_{i}"
            all_chunks.extend(chunks)
        return all_chunks

