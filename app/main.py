from fastapi import FastAPI

import models
from database import engine
from router import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)
