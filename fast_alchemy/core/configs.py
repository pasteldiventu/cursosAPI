from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import List


class Settings(BaseSettings):
# configurações  gerais usadas na aplicação

 API_V1_STR: str = '/api/v1'
 DB_URL: str = "postgresql+asyncpg://postgres:1509@localhost:5432/faculdade"
 DBBaseModel = declarative_base()


 class Config:
    case_sensitive = True


settings = Settings()
