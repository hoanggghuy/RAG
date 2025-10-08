from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
#VECTOR DB
    app_name: str
    qdrant_host: str
    qdrant_port: int
    COLLECTION_NAME: str
    EMBEDDING_DIR: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = Settings()