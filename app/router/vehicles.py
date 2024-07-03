from datetime import datetime
from typing import Annotated

from app.models import Vehicles
from starlette import status
from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel, Field
from requests import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.router.users import get_current_user

router = APIRouter(prefix='/vehicles', tags=['Vehicles'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dep = Annotated[Session, Depends(get_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


class CreateVehicleRequest(BaseModel):
    plate: str = Field(min_length=6, max_length=8)
    color: str = Field(min_length=1, max_length=10)
    brand: str = Field(min_length=1, max_length=20)


@router.post('/', status_code=status.HTTP_200_OK)
async def add_vehicle(db: db_dep, user: user_dep, request: CreateVehicleRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')

    existing_vehicle = db.query(Vehicles).filter(Vehicles.plate == request.plate).first()

    if existing_vehicle:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Vehicle with same plate already registered')

    create_vehicle = Vehicles(**request.model_dump(), owner_id=user.get('id'))
    db.add(create_vehicle)
    db.commit()
