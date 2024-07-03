from fastapi import FastAPI
import uvicorn
from app.router import auth, users

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
