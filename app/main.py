from fastapi import FastAPI
import uvicorn

from app import models
from app.database import engine
from app.router import auth, users, infractions


app = FastAPI()

app.include_router(auth.router)
app.include_router(infractions.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
