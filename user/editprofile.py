from fastapi import APIRouter, HTTPException, Depends
from user.user_schemas import EditProfileForm
from user.auth import get_current_user, get_user_exception
from database.models import Users
from database.session import get_db
from sqlalchemy.orm.session import Session


router = APIRouter(
    prefix="/edit", tags=["profile"], responses={401: {"user": "Not authorized"}}
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

    user_model.first_name = edit.first_name
    user_model.last_name = edit.last_name
    user_model.email = edit.email
    user_model.birth_date = edit.birth_date
    user_model.avatar = edit.avatar
    user_model.description = edit.description

    db.add(user_model)
    db.commit()

    return successful_response(200)


def successful_response(status_code: int):
    return {"status": 200, "transaction": "Successful"}


def http_exception():
    return HTTPException(status_code=404, detail="Todo not found!")
