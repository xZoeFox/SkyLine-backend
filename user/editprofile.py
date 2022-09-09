from fastapi import APIRouter, HTTPException, Depends
from user.register import get_password_hash
from user.user_schemas import EditProfileForm, ShowMyProfileForm, ShowProfileForm
from user.auth import get_current_user, get_user_exception, verify_password
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session
from sqlalchemy import exc


router = APIRouter(
    prefix="/profile", tags=["profile"], responses={401: {"user": "Not authorized"}}
)


# Route for profile edit:


@router.put("/")
async def profile_update(
    edit: EditProfileForm,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise get_user_exception()
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    if user_model is None:
        raise http_exception()

    if edit.first_name:
        user_model.first_name = edit.first_name

    if edit.last_name:
        user_model.last_name = edit.last_name

    if edit.email:
        user_model.email = edit.email

    if edit.birth_date:
        user_model.birth_date = edit.birth_date

    if edit.avatar:
        user_model.avatar = edit.avatar

    if edit.description:
        user_model.description = edit.description

    old_password = edit.old_password

    new_password = edit.new_password

    repeat_password = edit.repeat_password

    if old_password and user_model.password:
        if verify_password(old_password, user_model.password):
            if new_password == repeat_password:
                user_model.password = get_password_hash(new_password)
            else:
                return unsuccessful_response(400)
        else:
            return unsuccessful_response(400)

    try:
        db.add(user_model)
        db.commit()
        return successful_response(200)

    except exc.SQLAlchemyError as e:
        db.rollback()
        return unsuccessful_response(400)


# Route to get (logged) user profile (Login required):


@router.get("/myprofile")
async def get_myprofile(
    user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    result = db.query(Users).filter(Users.id == user.get("id")).first()

    return ShowMyProfileForm(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        email=result.email,
        birth_date=result.birth_date,
        avatar=result.avatar,
        description=result.description,
    )


# Route to get specific user profile by id (Login required):


@router.get("/{id}")
async def get_profile(
    id: int, user: dict = Depends(get_current_user), db: Session = Depends(get_db)
):

    if user is None:
        raise get_user_exception()

    result = db.query(Users).filter(Users.id == id).first()

    return ShowProfileForm(
        id=result.id,
        first_name=result.first_name,
        last_name=result.last_name,
        birth_date=result.birth_date,
        avatar=result.avatar,
        description=result.description,
    )


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}


def unsuccessful_response(status_code: int):
    return {"status": 400, "transaction": "Unsuccessful"}


def http_exception():
    return HTTPException(status_code=404, detail="User not found!")
