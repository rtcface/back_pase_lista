import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Base settings."""
    # FastAPI
    # Debug should be set to False in production
    DEBUG: Optional[bool] = os.getenv("DEBUG") == "True"
    # Title is the name of the application
    TITLE: Optional[str] = os.getenv("TITLE")
    #JWT
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    #CORS
    CORS_ALLOWED_ORIGINS: Optional[str] = os.getenv("CORS_ALLOWED_ORIGINS")
    #DatabasePostgres
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: Optional[str] = os.getenv("POSTGRES_PORT")
    POSTGRES_DB_DRIVER: Optional[str] = os.getenv("POSTGRES_DB_DRIVER")


settings = Settings()

