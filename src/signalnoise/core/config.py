from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    MODEL_NAME: str
    GROQ_API_KEY: str
    GROQ_TEMPERATURE: float
    GROQ_MODEL_NAME: str
    LANGCHAIN_API_KEY: str
    LANGCHAIN_TRACING_V2: bool = True
    LANGCHAIN_PROJECT: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql://"
            f"{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:"
            f"{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Backward compatibility alias
settings = get_settings()


