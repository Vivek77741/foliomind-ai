import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SNAPTRADE_CLIENT_ID: str = os.getenv("SNAPTRADE_CLIENT_ID", "DEMO_CLIENT_ID")
    SNAPTRADE_CONSUMER_KEY: str = os.getenv("SNAPTRADE_CONSUMER_KEY", "DEMO_CONSUMER_KEY")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")

    class Config:
        env_file = ".env"

settings = Settings()
