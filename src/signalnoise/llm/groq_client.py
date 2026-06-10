from langchain_groq import ChatGroq
from signalnoise.core.config import settings

class GroqClient:
    def __init__(self):
        self.client = ChatGroq(api_key=settings.GROQ_API_KEY, model=settings.GROQ_MODEL_NAME)

    @staticmethod
    def get_llm():
        return ChatGroq(
            model=settings.GROQ_MODEL_NAME,
            temperature=settings.GROQ_TEMPERATURE,
            max_tokens=1000,
            api_key=settings.GROQ_API_KEY
        )

    @staticmethod
    def get_response(query: str):
        response=GroqClient.get_llm().invoke(query)
        return response

