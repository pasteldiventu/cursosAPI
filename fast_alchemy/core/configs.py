from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base
from typing import List


class Settings(BaseSettings):
# configurações  gerais usadas na aplicação

 API_V1_STR: str = '/api/v1'
 DB_URL: str = "postgresql+asyncpg://postgres:ssW1T68NHbWpNgLH@abundantly-luminous-frog.data-1.use1.tembo.io:5432/postgres"
 DBBaseModel = declarative_base()


 class Config:
    case_sensitive = True


settings = Settings()
