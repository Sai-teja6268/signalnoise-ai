from dotenv import load_dotenv
import os
load_dotenv()

class settings:
    MODEL_NAME=os.getenv("MODEL_NAME")
    LANGCHAIN_API_KEY=os.getenv("LANGCHAIN_API_KEY")
    LANGCHAIN_TRACING_V2=os.getenv("LANGCHAIN_TRACING_V2")
    LANGCHAIN_PROJECT=os.getenv("LANGCHAIN_PROJECT")
    POSTGRES_HOST=os.getenv("POSTGRES_HOST")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT")
    POSTGRES_DB=os.getenv("POSTGRES_DB")
    POSTGRES_USER=os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")

settings = settings()

