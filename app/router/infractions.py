from datetime import datetime
from typing import Annotated
from starlette import status
from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel, Field
from requests import Session
from passlib.context import CryptContext
from app.database import SessionLocal
from app.models import Infractions, Users
from app.router.users import get_current_user, UsersRoles

router = APIRouter(prefix='/infractions', tags=['Infractions'])

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
    vehicle_plate: str = Field(min_length=6, max_length=8)  # length of car plates IDs in Argentina
    timestamp: datetime = Field(gt=0)
    comments: str


@router.post('/', status_code=status.HTTP_200_OK)
async def register_new_infraction(db: db_dep, user: user_dep, request: CreateInfractionRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Authentication failed')
    elif user.get('role') != UsersRoles.POLICE_OFFICER:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    create_infraction = Infractions(infractor_id=user.get('id'), **request.model_dump())
    db.add(create_infraction)
    db.commit()


@router.get('/{email}', status_code=status.HTTP_200_OK)
async def generate_report(db: db_dep, email: str):
    person = db.query(Users).filter(Users.email == email).first()
    infractions = []
    if person:
        infractions = db.query(Infractions).filter(Infractions.infractor_id == person.id)
    return infractions



