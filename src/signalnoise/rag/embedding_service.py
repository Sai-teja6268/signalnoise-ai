from langchain_huggingface import HuggingFaceEmbeddings
from signalnoise.core.config import settings

class EmbeddingService():
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name= settings.MODEL_NAME
        )

    def get_embeddings(self):
        return self.embeddings

EMBEDDINGS = EmbeddingService().get_embeddings()