from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):

    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(60, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    REFRESH_TOKEN_EXPIRE_MINUTES:int = Field(60*24*7, env="REFRESH_TOKEN_EXPIRE_MINUTES")
    TOKEN_ALGO: str = Field('HS256', env="TOKEN_ALGO")
    JWT_KEY: str = Field(..., env="JWT_KEY")
    JWT_REFRESH_KEY: str = Field(..., env="JWT_REFRESH_KEY")

    class Config:
        env_file = Path(__file__).parents[1].joinpath(".env")
        env_file_encoding = "utf-8"
