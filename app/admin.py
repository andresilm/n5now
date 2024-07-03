from .database import SessionLocal
from .models import Users
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = '1234'


def create_admin():
    db = SessionLocal()
    admin_user = Users(username=ADMIN_USERNAME,
                       hashed_password=bcrypt_context.hash(ADMIN_PASSWORD),
                       role='admin')
    db.add(admin_user)
    db.commit()
    db.close()


