from fastapi import APIRouter, Depends, status, HTTPException
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session
from user.user_schemas import RegisterForm
from datetime import date
from passlib.context import CryptContext

router = APIRouter(
    prefix="/register", tags=["sign-up"], responses={401: {"user": "Not authorized"}}
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password function:


def get_password_hash(password):
    return bcrypt_context.hash(password)


# Route for user registration:


@router.post("/")
async def user_registration(reg: RegisterForm, db: Session = Depends(get_db)):
    user = Users()
    user.first_name = reg.first_name.capitalize()
    user.last_name = reg.last_name.capitalize()
    user.email = reg.email

    hash_password = get_password_hash(reg.password)
    user.password = hash_password

    repeat_password = reg.password_repeat

    user.date_joined = date.today()
    user.active = True

    if repeat_password == reg.password:
        db.add(user)
        db.commit()
        return successful_response(201)
    else:
        return unsuccessful_response(400)


# Response (status & message):


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}


def unsuccessful_response(status_code: int):
    return {"status": 400, "transaction": "Unsuccessful"}
