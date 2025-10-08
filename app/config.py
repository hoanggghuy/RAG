from pydantic_settings import BaseSettings
from functools import lru_cache
class Settings(BaseSettings):
#VECTOR DB
    app_name: str
    QDRANT_HOST: str
    QDRANT_PORT: int
    COLLECTION_NAME: str
    EMBEDDING_DIR: str

    class Config:
        env_file = r"C:\Users\ADMIN\Desktop\DATK1\.env"
        env_file_encoding = "utf-8"

@lru_cache()
def get_settings() -> Settings:
    return Settings()

