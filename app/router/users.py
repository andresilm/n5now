from typing import Annotated
from jose import jwt, JWTError
from fastapi import Depends, APIRouter, HTTPException
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from requests import Session
from starlette import status
from database import SessionLocal
from models import Users
from router.auth import SECRET_KEY, ALGORITHM

router = APIRouter(prefix='/users', tags=['Users'])

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        if not username or not user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not authenticate user')
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Could not authenticate user')


db_dep = Annotated[Session, Depends(get_db)]
user_dep = Annotated[dict, Depends(get_current_user)]


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dep, create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role,
        is_active=True
    )
    db.add(create_user_model)
    db.commit()


@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dep, db: db_dep):
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 'Authentication failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


@router.post('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user_verification: UserVerification, user: user_dep, db: db_dep):
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    else:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Authentication failed: wrong password')
    db.add(user_model)
    db.commit()
