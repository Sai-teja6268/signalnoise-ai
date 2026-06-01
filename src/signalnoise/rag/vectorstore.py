from langchain_chroma import Chroma
from signalnoise.rag.embedding_service import EMBEDDINGS

class VectorStore:
    def __init__(self, embedding_model=EMBEDDINGS):
        self.vectorstore = Chroma(
            embedding_function=embedding_model,
            collection_name="signalnoise",
            persist_directory="./chroma_db"
        )

    def add_documents(self, documents):
        return self.vectorstore.add_documents(documents)

    def similarity_search_with_score(self, query: str, k: int = 5):
        return self.vectorstore.similarity_search_with_score(query, k=k)

    def get_vectorstore(self):
        return self.vectorstore