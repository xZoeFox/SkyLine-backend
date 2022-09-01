from fastapi import APIRouter, Depends
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session
from user.user_schemas import RegisterForm


router = APIRouter(
    prefix="/register",
    tags=["sign-up"],
    responses={401: {"user": "Not authorized"}}
)

@router.post("/")
async def register_user(reg: RegisterForm, db: Session = Depends(get_db)):
    user = Users()
    user.first_name = reg.first_name
    user.last_name = reg.last_name
    user.email = reg.email
    user.password = reg.password
    user.date_joined = reg.date_joined
    user.birth_date = reg.birth_date
    user.avatar = reg.avatar
    user.description = reg.description
    user.active = reg.acive

    db.add(user)
    db.commit()

    return successful_response(201)

def successful_response(status_code: int):
    return {
        "status": 200,
        "transaction":"Successful"
    }