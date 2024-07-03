from datetime import datetime
from typing import Annotated
from starlette import status
from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel, Field
from requests import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import Infractions
from app.router.users import get_current_user

router = APIRouter(prefix='/infractions', tags=['Users'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


class CreateInfractionRequest(BaseModel):
    vehicle_plate: str = Field(min_length=6, max_length=8)  # lengths of car plates IDs in Argentina
    timestamp: datetime = Field(gt=0)
    comments: str


@router.post('/', status_code=status.HTTP_200_OK)
async def cargar_infraccion(db: db_dep, user: user_dep, request: CreateInfractionRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    infraction = Infractions(**request.dict(), id=user.get('id'))


@router.post('/', status_code=status.HTTP_200_OK)
async def generar_informe(db: db_dep):
    pass


