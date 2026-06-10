from langchain_chroma import Chroma
from signalnoise.rag.embedding_service import EMBEDDINGS

class VectorStore:
    def __init__(self, embedding_model=EMBEDDINGS):
        self.vectorstore = Chroma(
            embedding_function=embedding_model,
            collection_name="signalnoise",
            persist_directory="./chroma_db"
        )

    def add_documents(self, documents, ids=None):
        return self.vectorstore.add_documents(documents, ids=ids)

    def similarity_search_with_score(self, query: str, k: int = 5, filter: dict = None):
        import time
        max_retries = 3
        delay = 1.0
        for attempt in range(max_retries):
            try:
                return self.vectorstore.similarity_search_with_score(query, k=k, filter=filter)
            except Exception as e:
                if "finding id" in str(e).lower() and attempt < max_retries - 1:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise e

    def get_vectorstore(self):
        return self.vectorstore