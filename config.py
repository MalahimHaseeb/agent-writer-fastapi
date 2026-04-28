"""Application configuration management."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_ENV: str = "development"
    DEBUG: bool = True

    APP_NAME: str = "Blog Writer Agent"
    APP_VERSION: str = "1.0.0"

    GEMINI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""

    LLM_MODEL: str = "gemini-2.5-flash"
    LLM_TIMEOUT: int = 60

    SEARCH_MAX_RESULTS: int = 5
    SEARCH_DEPTH: str = "basic"

    MIN_TOPIC_LENGTH: int = 3
    MIN_BLOG_WORD_COUNT: int = 600

    class Config:
        env_file = ".env"
        case_sensitive = True

    def validate_api_keys(self) -> bool:
        if not self.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured")
        if not self.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY is not configured")
        return True


@lru_cache()
def get_settings() -> Settings:
    settings = Settings()
    return settings
