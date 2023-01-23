from fastapi import FastAPI

from settings.settings import Settings
from db.models import BaseModel
from db.database import SessionLocal, engine
from routers.api import api_router

settings = Settings()

app = FastAPI();
app.include_router(api_router)

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();

@app.on_event("startup")
def startup():
    BaseModel.metadata.create_all(bind=engine)


def main():
    run(app, port=settings.PORT)


if __name__ == "__main__":
    main()
