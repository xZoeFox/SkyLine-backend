from fastapi import APIRouter, Depends, status, HTTPException
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session
from user.user_schemas import LoginForm
from datetime import date
from passlib.context import CryptContext

router = APIRouter(
    prefix="/login",
    tags=["sign-in"],
    responses={401: {"user": "Not authorized"}}
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify password function:

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(
        plain_password, hashed_password
    ) 

@router.post("/")
def authenticate_user(lg: LoginForm, db: Session = Depends(get_db)):  
    
    user = db.query(Users).filter(Users.email == lg.email).first()

    if not user:
        return login_exception()
    
    if not verify_password(lg.password, user.password):
        return login_exception()
    
    return user

def login_exception():
    login_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
    )
    return login_exception_response