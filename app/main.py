from fastapi import FastAPI

from db.models import BaseModel
from db.database import SessionLocal, engine
from routers.api import api_router


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
    run(app, port=8000)


if __name__ == "__main__":
    main()
