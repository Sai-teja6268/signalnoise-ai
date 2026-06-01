from langchain_core.documents import Document
from signalnoise.ingestion.schema import EnterpriseDocument

class DocumentProcessor:
    def process_documents(self,documents:list[EnterpriseDocument]) -> list[Document]:
        langchain_docs = []
        for doc in documents:
            langchain_docs.append(
                Document(
                    page_content=doc.content,
                    metadata={
                        "document_id": doc.document_id,
                        "source": doc.source,
                        "team": doc.team,
                        "department": doc.department,
                        "date": doc.date,
                        "ingestion_timestamp": doc.ingestion_timestamp.isoformat() if doc.ingestion_timestamp else None
                    }
                )
            )
        return langchain_docs
        