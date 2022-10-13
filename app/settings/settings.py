from pydantic import BaseSettings, Field
from pathlib import Path

class Settings(BaseSettings):

    DB_NAME: str = Field(..., env="DB_NAME")
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASSWORD: str = Field(..., env="DB_PASSWORD")
    DB_HOST: str = Field(..., env="DB_HOST")

    class Config:
        env_file = Path(__file__).parents[1].joinpath(".env")
        env_file_encoding = "utf-8"
