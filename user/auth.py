from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, status, HTTPException, APIRouter
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

router = APIRouter(
    prefix="/auth", tags=["sign-in"], responses={401: {"user": "Not authorized"}}
)

load_dotenv()
SECRET_KEY: str = os.getenv("SECRET_KEY")
ALGORITHM: str = os.getenv("ALGORITHM")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Verify password function:

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)

# To check if user is logged in:

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("id")

        if email is None or user_id is None:
            raise get_user_exception()

        return {"email": email, "id": user_id}

    except:
        raise get_user_exception()

# Function for JWT creation:

def create_access_token(
    email: str, user_id: int, expires_delta: Optional[timedelta] = None
):

    encode = {"sub": email, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

# Check if email & password match:

def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):

    user = db.query(Users).filter(Users.email == email).first()

    if not user:
        return False

    if not verify_password(password, user.password):
        return False

    return user


# Route to get token by login:

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):

    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.email, user.id, expires_delta=token_expires)

    return {"token": token}


# Custom Exceptions:


def get_user_exception():
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return credentials_exception


def token_exception():
    token_exception_response = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return token_exception_response
