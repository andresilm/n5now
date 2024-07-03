from fastapi import FastAPI
import uvicorn

from app import models
from app.admin import create_admin, ADMIN_USERNAME, ADMIN_PASSWORD
from app.database import engine, SQLALCHEMY_DB_URL
from app.models import Vehicles, Infractions, Citizens
from app.router import auth, users
from fastapi_admin.app import app as admin_app
from fastapi_admin.providers.login import UsernamePasswordProvider
from fastapi_admin.template import templates
from fastapi_admin.resources import Model


app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)

models.Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def startup():

    await admin_app.configure(
        app,
        database_url=SQLALCHEMY_DB_URL,
        providers=[
            UsernamePasswordProvider(
                login_url="/admin/login",
                secret_key="your-secret-key",
                username_field=ADMIN_USERNAME,
                password_field=ADMIN_PASSWORD,
            )
        ],
    )

    admin_app.register_resources([
        Model(Citizens, templates.Template),
        Model(Infractions, templates.Template),
        Model(Vehicles, templates.Template),
    ])

app.mount("/admin", admin_app)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
