from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Depends

from settings import Settings

# def get_settings():
#     return Settings()

settings = Settings()

db_connection_str = f"postgresql://"\
                 f"{settings.DB_USER}:{settings.DB_PASSWORD}@" \
                 f"{settings.DB_HOST}/{settings.DB_NAME}"

#db_connection_str = 'mysql+mysqlconnector://superuser:password@localhost/test1';
#db_connection_str = 'postgresql://postgres:3141592653589@postgresserver/test1'

engine = create_engine(db_connection_str);

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);
