import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl
from dotenv import dotenv_values

_env = dotenv_values(".env")  # does nothing if file absent

class Settings(BaseSettings):
    database_url: AnyUrl = os.getenv("DATABASE_URL", "sqlite:///./boatable.db")
    neo4j_uri: AnyUrl = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
    elastic_uri: AnyUrl = os.getenv("ELASTIC_URI", "http://elasticsearch:9200")
    secret_key: str = os.getenv("SECRET_KEY", "dev")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:  # pragma: no cover
    return Settings()
