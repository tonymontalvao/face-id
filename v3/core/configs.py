from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    # Configurações gerais usadas na aplicação
    DB_URL: str = "sqlite:///faceid.db"

    class Config:
        case_sensitive = True


settings = Settings()
DBBaseModel = declarative_base()
